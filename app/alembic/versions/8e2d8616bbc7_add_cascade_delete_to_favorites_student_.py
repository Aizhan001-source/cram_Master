"""add cascade delete to favorites.student_id

Revision ID: 8e2d8616bbc7
Revises: 94c6da09ccbe
Create Date: 2026-05-04 16:46:24.826901

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8e2d8616bbc7'
down_revision: Union[str, Sequence[str], None] = '94c6da09ccbe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_constraint(
        "favorites_student_id_fkey",  # ⚠️ проверь имя!
        "favorites",
        type_="foreignkey"
    )

    op.create_foreign_key(
        "favorites_student_id_fkey",
        "favorites",
        "students",
        ["student_id"],
        ["id"],
        ondelete="CASCADE"  # 🔥 ключевая строка
    )


def downgrade():
    op.drop_constraint(
        "favorites_student_id_fkey",
        "favorites",
        type_="foreignkey"
    )

    op.create_foreign_key(
        "favorites_student_id_fkey",
        "favorites",
        "students",
        ["student_id"],
        ["id"]
        # без cascade — откат
    )