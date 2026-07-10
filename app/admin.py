from functools import wraps

from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for

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
        SELECT student_id, week_number, submission_url, submitted_at, updated_at
        FROM submissions
        """
    ).fetchall()

    submissions_by_student = {
        (submission["student_id"], submission["week_number"]): submission
        for submission in submissions
    }

    return render_template(
        "admin/dashboard.html",
        students=students,
        weeks=WEEKS,
        submissions_by_student=submissions_by_student,
    )