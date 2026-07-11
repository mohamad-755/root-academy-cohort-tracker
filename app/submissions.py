from flask import Blueprint, abort, flash, g, redirect, render_template, request, url_for

from app.auth import login_required
from app.curriculum import WEEKS
from app.extensions import db
from app.models import Submission


submissions = Blueprint("submissions", __name__, url_prefix="/submissions")


def get_week_or_404(week_number):
    week = next((item for item in WEEKS if item["number"] == week_number), None)

    if week is None:
        abort(404)

    return week

@submissions.route("/week/<int:week_number>", methods=("GET", "POST"))
@login_required
def submit(week_number):
    week = get_week_or_404(week_number)

    existing_submission = Submission.query.filter_by(
        student_id=g.student.id,
        week_number=week_number,
    ).first()

    if request.method == "POST":
        submission_url = request.form["submission_url"].strip()
        note = request.form["note"].strip()
        error = None

        if not submission_url:
            error = "Submission link is required."

        if error is None:
            if existing_submission is None:
                submission = Submission(
                    student_id=g.student.id,
                    week_number=week_number,
                    submission_url=submission_url,
                    note=note,
                )
                db.session.add(submission)
                flash("Submission saved.")
            else:
                existing_submission.submission_url = submission_url
                existing_submission.note = note
                flash("Submission updated.")

            db.session.commit()
            return redirect(url_for("curriculum.week_detail", week_number=week_number))

        flash(error)

    return render_template(
        "submissions/submit.html",
        week=week,
        submission=existing_submission,
    )
