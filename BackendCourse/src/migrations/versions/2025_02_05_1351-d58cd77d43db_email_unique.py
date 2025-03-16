"""email unique

Revision ID: d58cd77d43db
Revises: 15f5ae87b607
Create Date: 2025-02-05 13:51:13.190359

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa  # noqa: F401


# revision identifiers, used by Alembic.
revision: str = "d58cd77d43db"
down_revision: Union[str, None] = "15f5ae87b607"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
