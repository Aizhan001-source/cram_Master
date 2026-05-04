"""add cascade delete to bookings.student_id

Revision ID: 94c6da09ccbe
Revises: 6e15acf923c3
Create Date: 2026-05-04 16:40:14.625067

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '94c6da09ccbe'
down_revision: Union[str, Sequence[str], None] = '6e15acf923c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_constraint("bookings_student_id_fkey", "bookings", type_="foreignkey")

    op.create_foreign_key(
        "bookings_student_id_fkey",
        "bookings",
        "students",
        ["student_id"],
        ["id"],
        ondelete="CASCADE"
    )


def downgrade():
    op.drop_constraint("bookings_student_id_fkey", "bookings", type_="foreignkey")

    op.create_foreign_key(
        "bookings_student_id_fkey",
        "bookings",
        "students",
        ["student_id"],
        ["id"]
    )