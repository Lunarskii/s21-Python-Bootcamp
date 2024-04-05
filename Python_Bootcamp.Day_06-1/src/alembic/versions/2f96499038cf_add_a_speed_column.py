"""Add a speed column

Revision ID: 2f96499038cf
Revises: 1e70cd8b0464
Create Date: 2024-02-15 14:16:29.800437

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2f96499038cf'
down_revision: Union[str, None] = '1e70cd8b0464'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        'ships',
        sa.Column('speed', sa.Integer)
    )


def downgrade() -> None:
    op.drop_column('ships', 'speed')
