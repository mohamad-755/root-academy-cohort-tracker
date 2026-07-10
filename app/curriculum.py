from flask import Blueprint, abort, render_template

from app.auth import login_required


curriculum = Blueprint("curriculum", __name__, url_prefix="/curriculum")


WEEKS = [
    {
        "number": 1,
        "title": "Introduction to Data Science",
        "summary": "Get oriented with the cohort, the data science workflow, and the tools students will use throughout the course.",
        "objectives": [
            "Understand what data science is and where it is used",
            "Set up the course workflow and expectations",
            "Practice reading a simple dataset",
        ],
        "tasks": [
            "Review the cohort welcome materials",
            "Set up your Python environment",
            "Complete the Week 1 reflection",
        ],
    },
    {
        "number": 2,
        "title": "Python Foundations for Data",
        "summary": "Build confidence with Python basics used in data analysis, including variables, lists, dictionaries, and simple functions.",
        "objectives": [
            "Use Python variables and data types",
            "Work with lists and dictionaries",
            "Write small functions for repeated logic",
        ],
        "tasks": [
            "Complete the Python foundations notebook",
            "Practice list and dictionary exercises",
            "Submit your Week 2 checkpoint",
        ],
    },
]


@curriculum.route("/")
@login_required
def index():
    return render_template("curriculum/index.html", weeks=WEEKS)


@curriculum.route("/week/<int:week_number>")
@login_required
def week_detail(week_number):
    week = next((item for item in WEEKS if item["number"] == week_number), None)

    if week is None:
        abort(404)

    return render_template("curriculum/week.html", week=week)