from flask import Blueprint, g, render_template

from app.curriculum import WEEKS
from app.db import get_db


main = Blueprint("main", __name__)


@main.route("/")
def index():
    progress = None

    if g.student:
        db = get_db()
        submitted_count = db.execute(
            """
            SELECT COUNT(*) AS count
            FROM submissions
            WHERE student_id = ?
            """,
            (g.student.id,),
        ).fetchone()["count"]

        total_weeks = len(WEEKS)
        percentage = round((submitted_count / total_weeks) * 100) if total_weeks else 0

        progress = {
            "submitted_count": submitted_count,
            "total_weeks": total_weeks,
            "percentage": percentage,
        }

    return render_template("index.html", progress=progress)