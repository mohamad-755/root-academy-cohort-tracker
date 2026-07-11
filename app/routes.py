from flask import Blueprint, g, render_template

from app.curriculum import WEEKS
from app.models import Submission


main = Blueprint("main", __name__)


@main.route("/")
def index():
    progress = None

    if g.student:
        submitted_count = Submission.query.filter_by(student_id=g.student.id).count()

        total_weeks = len(WEEKS)
        percentage = round((submitted_count / total_weeks) * 100) if total_weeks else 0

        progress = {
            "submitted_count": submitted_count,
            "total_weeks": total_weeks,
            "percentage": percentage,
        }

    return render_template("index.html", progress=progress)
