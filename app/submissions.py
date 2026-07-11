from flask import Blueprint, abort, flash, g, redirect, render_template, request, url_for

from app.auth import login_required
from app.curriculum import WEEKS
from app.db import get_db


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
    db = get_db()

    existing_submission = db.execute(
        """
        SELECT * FROM submissions
        WHERE student_id = ? AND week_number = ?
        """,
        (g.student.id, week_number),
    ).fetchone()

    if request.method == "POST":
        submission_url = request.form["submission_url"].strip()
        note = request.form["note"].strip()
        error = None

        if not submission_url:
            error = "Submission link is required."

        if error is None:
            if existing_submission is None:
                db.execute(
                    """
                    INSERT INTO submissions (student_id, week_number, submission_url, note)
                    VALUES (?, ?, ?, ?)
                    """,
                    (g.student.id, week_number, submission_url, note),
                )
                flash("Submission saved.")
            else:
                db.execute(
                    """
                    UPDATE submissions
                    SET submission_url = ?, note = ?, updated_at = CURRENT_TIMESTAMP
                    WHERE id = ?
                    """,
                    (submission_url, note, existing_submission["id"]),
                )
                flash("Submission updated.")

            db.commit()
            return redirect(url_for("curriculum.week_detail", week_number=week_number))

        flash(error)

    return render_template(
        "submissions/submit.html",
        week=week,
        submission=existing_submission,
    )