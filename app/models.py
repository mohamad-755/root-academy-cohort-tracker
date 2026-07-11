from datetime import datetime, timezone

from app.extensions import db


def utc_now():
    return datetime.now(timezone.utc)


class Student(db.Model):
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    cohort_code = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=utc_now)

    submissions = db.relationship(
        "Submission",
        back_populates="student",
        cascade="all, delete-orphan",
    )


class Submission(db.Model):
    __tablename__ = "submissions"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    week_number = db.Column(db.Integer, nullable=False)
    submission_url = db.Column(db.Text, nullable=False)
    note = db.Column(db.Text)
    feedback = db.Column(db.Text)
    submitted_at = db.Column(db.DateTime, nullable=False, default=utc_now)
    updated_at = db.Column(
        db.DateTime,
        nullable=False,
        default=utc_now,
        onupdate=utc_now,
    )
    reviewed_at = db.Column(db.DateTime)

    student = db.relationship("Student", back_populates="submissions")

    __table_args__ = (
        db.UniqueConstraint("student_id", "week_number", name="unique_student_week"),
    )
