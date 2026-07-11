from functools import wraps
from datetime import datetime, timezone

from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, session, url_for
from flask_mail import Message
from sqlalchemy import and_, or_

from app.curriculum import WEEKS
from app.extensions import db
from app.mail import mail
from app.models import Student, Submission


admin = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if not session.get("is_admin"):
            return redirect(url_for("admin.login"))

        return view(**kwargs)

    return wrapped_view


@admin.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        admin_code = request.form["admin_code"].strip()

        if admin_code == current_app.config["ADMIN_CODE"]:
            session.clear()
            session["is_admin"] = True
            return redirect(url_for("admin.dashboard"))

        flash("Incorrect admin code.")

    return render_template("admin/login.html")


@admin.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.index"))


@admin.route("/")
@admin_required
def dashboard():
    search = request.args.get("search", "").strip()
    students_query = Student.query

    if search:
        search_pattern = f"%{search}%"
        students_query = students_query.filter(
            or_(
                Student.name.ilike(search_pattern),
                Student.email.ilike(search_pattern),
            )
        )

    students = students_query.order_by(Student.created_at.desc()).all()
    submissions = Submission.query.all()

    submissions_by_student = {
        (submission.student_id, submission.week_number): submission
        for submission in submissions
    }

    progress_by_student = {}

    for student in students:
        submitted_count = sum(
            1
            for week in WEEKS
            if (student.id, week["number"]) in submissions_by_student
        )
        total_weeks = len(WEEKS)
        percentage = round((submitted_count / total_weeks) * 100) if total_weeks else 0

        progress_by_student[student.id] = {
            "submitted_count": submitted_count,
            "total_weeks": total_weeks,
            "percentage": percentage,
        }

    return render_template(
        "admin/dashboard.html",
        students=students,
        weeks=WEEKS,
        submissions_by_student=submissions_by_student,
        progress_by_student=progress_by_student,
        search=search,
    )


@admin.route("/submissions/<int:submission_id>/review", methods=("GET", "POST"))
@admin_required
def review_submission(submission_id):
    submission = db.session.get(Submission, submission_id)

    if submission is None:
        abort(404)

    if request.method == "POST":
        feedback = request.form["feedback"].strip()

        submission.feedback = feedback
        submission.reviewed_at = datetime.now(timezone.utc)
        db.session.commit()

        flash("Feedback saved.")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/review_submission.html", submission=submission)


@admin.route("/reminders/week/<int:week_number>", methods=("POST",))
@admin_required
def send_reminders(week_number):
    week = next((item for item in WEEKS if item["number"] == week_number), None)

    if week is None:
        abort(404)

    missing_students = (
        Student.query.outerjoin(
            Submission,
            and_(
                Submission.student_id == Student.id,
                Submission.week_number == week_number,
            ),
        )
        .filter(Submission.id.is_(None))
        .order_by(Student.name)
        .all()
    )

    for student in missing_students:
        message = Message(
            subject=f"Reminder: Week {week_number} submission",
            recipients=[student.email],
            body=(
                f"Hi {student.name},\n\n"
                f"This is a reminder to submit your work for Week {week_number}: {week['title']}.\n\n"
                "You can log in to the Root Academy Cohort Tracker to submit your work.\n\n"
                "Best,\n"
                "Root Academy"
            ),
        )
        mail.send(message)

    flash(f"Sent {len(missing_students)} reminder email(s) for Week {week_number}.")
    return redirect(url_for("admin.dashboard"))
