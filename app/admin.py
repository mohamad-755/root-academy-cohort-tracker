from functools import wraps

from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, session, url_for

from app.curriculum import WEEKS
from app.db import get_db


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
    db = get_db()

    students = db.execute(
        """
        SELECT id, name, email, created_at
        FROM students
        ORDER BY created_at DESC
        """
    ).fetchall()

    submissions = db.execute(
        """
        SELECT id, student_id, week_number, submission_url, submitted_at, updated_at, feedback
        FROM submissions
        """
    ).fetchall()

    submissions_by_student = {
        (submission["student_id"], submission["week_number"]): submission
        for submission in submissions
    }

    progress_by_student = {}

    for student in students:
        submitted_count = sum(
            1
            for week in WEEKS
            if (student["id"], week["number"]) in submissions_by_student
        )
        total_weeks = len(WEEKS)
        percentage = round((submitted_count / total_weeks) * 100) if total_weeks else 0

        progress_by_student[student["id"]] = {
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
    )


@admin.route("/submissions/<int:submission_id>/review", methods=("GET", "POST"))
@admin_required
def review_submission(submission_id):
    db = get_db()

    submission = db.execute(
        """
        SELECT submissions.*, students.name AS student_name, students.email AS student_email
        FROM submissions
        JOIN students ON submissions.student_id = students.id
        WHERE submissions.id = ?
        """,
        (submission_id,),
    ).fetchone()

    if submission is None:
        abort(404)

    if request.method == "POST":
        feedback = request.form["feedback"].strip()

        db.execute(
            """
            UPDATE submissions
            SET feedback = ?, reviewed_at = CURRENT_TIMESTAMP
            WHERE id = ?
            """,
            (feedback, submission_id),
        )
        db.commit()

        flash("Feedback saved.")
        return redirect(url_for("admin.dashboard"))

    return render_template("admin/review_submission.html", submission=submission)