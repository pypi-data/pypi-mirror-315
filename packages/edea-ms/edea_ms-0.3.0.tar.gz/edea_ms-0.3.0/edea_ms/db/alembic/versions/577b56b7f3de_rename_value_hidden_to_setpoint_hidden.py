"""rename value_hidden to setpoint_hidden

Revision ID: 577b56b7f3de
Revises: a73209e4df83
Create Date: 2024-10-29 12:32:05.286497

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '577b56b7f3de'
down_revision: Union[str, None] = 'a73209e4df83'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.alter_column('forcing_conditions', 'value_hidden', new_column_name="setpoint_hidden")


def downgrade() -> None:
    op.alter_column('forcing_conditions', 'setpoint_hidden', new_column_name="value_hidden")
