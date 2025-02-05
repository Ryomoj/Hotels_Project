"""add users

Revision ID: 15f5ae87b607
Revises: 44feac4ad5cb
Create Date: 2025-02-05 13:01:39.608373

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "15f5ae87b607"
down_revision: Union[str, None] = "44feac4ad5cb"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("email", sa.String(length=200), nullable=False),
        sa.Column("hashed_password", sa.String(length=200), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users")
