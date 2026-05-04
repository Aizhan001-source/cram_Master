"""add cascade to course->schedule

Revision ID: 493bb37113f1
Revises: fe000f35f1c4
Create Date: 2026-05-05 02:17:04.266460

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '493bb37113f1'
down_revision: Union[str, Sequence[str], None] = 'fe000f35f1c4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    # удаляем старый FK
    op.drop_constraint(
        "schedules_course_id_fkey",
        "schedules",
        type_="foreignkey"
    )

    # создаём новый с CASCADE
    op.create_foreign_key(
        "schedules_course_id_fkey",
        "schedules",
        "courses",
        ["course_id"],
        ["id"],
        ondelete="CASCADE"
    )


def downgrade():
    # откат (без cascade)
    op.drop_constraint(
        "schedules_course_id_fkey",
        "schedules",
        type_="foreignkey"
    )

    op.create_foreign_key(
        "schedules_course_id_fkey",
        "schedules",
        "courses",
        ["course_id"],
        ["id"]
    )