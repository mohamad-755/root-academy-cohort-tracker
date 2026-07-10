import sqlite3
from functools import wraps

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for

from app.db import get_db

auth = Blueprint("auth", __name__)


@auth.before_app_request
def load_logged_in_student():
    student_id = session.get("student_id")

    if student_id is None:
        g.student = None
    else:
        g.student = get_db().execute(
            "SELECT * FROM students WHERE id = ?",
            (student_id,),
        ).fetchone()


@auth.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        cohort_code = request.form["cohort_code"].strip()

        db = get_db()
        error = None

        if not name:
            error = "Name is required."
        elif not email:
            error = "Email is required."
        elif not cohort_code:
            error = "Cohort code is required."

        if error is None:
            try:
                db.execute(
                    "INSERT INTO students (name, email, cohort_code) VALUES (?, ?, ?)",
                    (name, email, cohort_code),
                )
                db.commit()
            except sqlite3.IntegrityError:
                error = "A student with that email already exists."
            else:
                flash("Registration successful. Please log in.")
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template("auth/register.html")


@auth.route("/login", methods=("GET", "POST"))
def login():
    if request.method == "POST":
        email = request.form["email"].strip().lower()
        cohort_code = request.form["cohort_code"].strip()

        db = get_db()
        error = None

        student = db.execute(
            "SELECT * FROM students WHERE email = ? AND cohort_code = ?",
            (email, cohort_code),
        ).fetchone()

        if student is None:
            error = "Incorrect email or cohort code."

        if error is None:
            session.clear()
            session["student_id"] = student["id"]
            return redirect(url_for("main.index"))

        flash(error)

    return render_template("auth/login.html")


@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("main.index"))


def login_required(view):
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.student is None:
            return redirect(url_for("auth.login"))

        return view(**kwargs)

    return wrapped_view