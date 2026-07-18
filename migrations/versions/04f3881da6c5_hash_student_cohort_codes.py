"""Hash student cohort codes

Revision ID: 04f3881da6c5
Revises: 7fc5335279a3
Create Date: 2026-07-18 00:19:42.481048

"""
from alembic import op
import sqlalchemy as sa
from werkzeug.security import generate_password_hash


revision = '04f3881da6c5'
down_revision = '7fc5335279a3'
branch_labels = None
depends_on = None


def upgrade():
    with op.batch_alter_table('students', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cohort_code_hash', sa.String(length=255), nullable=True))

    connection = op.get_bind()
    students = connection.execute(sa.text("SELECT id, cohort_code FROM students")).fetchall()

    for student in students:
        connection.execute(
            sa.text(
                """
                UPDATE students
                SET cohort_code_hash = :cohort_code_hash
                WHERE id = :student_id
                """
            ),
            {
                "cohort_code_hash": generate_password_hash(student.cohort_code),
                "student_id": student.id,
            },
        )

    with op.batch_alter_table('students', schema=None) as batch_op:
        batch_op.alter_column('cohort_code_hash', nullable=False)
        batch_op.drop_column('cohort_code')


def downgrade():
    with op.batch_alter_table('students', schema=None) as batch_op:
        batch_op.add_column(sa.Column('cohort_code', sa.VARCHAR(length=80), nullable=True))
        batch_op.drop_column('cohort_code_hash')
