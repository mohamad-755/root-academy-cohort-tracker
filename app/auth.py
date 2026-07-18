from functools import wraps

from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from sqlalchemy.exc import IntegrityError

from app.extensions import db
from app.models import Student


auth = Blueprint("auth", __name__)


@auth.before_app_request
def load_logged_in_student():
    student_id = session.get("student_id")

    if student_id is None:
        g.student = None
    else:
        g.student = db.session.get(Student, student_id)


@auth.route("/register", methods=("GET", "POST"))
def register():
    if request.method == "POST":
        name = request.form["name"].strip()
        email = request.form["email"].strip().lower()
        cohort_code = request.form["cohort_code"].strip()

        error = None

        if not name:
            error = "Name is required."
        elif not email:
            error = "Email is required."
        elif not cohort_code:
            error = "Cohort code is required."

        if error is None:
            try:
                student = Student(name=name, email=email)
                student.set_cohort_code(cohort_code)
                db.session.add(student)
                db.session.commit()
            except IntegrityError:
                db.session.rollback()
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

        error = None

        student = Student.query.filter_by(email=email).first()

        if student is None or not student.check_cohort_code(cohort_code):
            error = "Incorrect email or cohort code."

        if error is None:
            session.clear()
            session["student_id"] = student.id
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