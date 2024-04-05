"""create tables of ships and officers

Revision ID: 1e70cd8b0464
Revises: 
Create Date: 2024-02-15 14:13:44.773546

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e70cd8b0464'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'ships',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('alignment', sa.String),
        sa.Column('name', sa.String),
        sa.Column('ship_class', sa.String),
        sa.Column('length', sa.Float),
        sa.Column('crew_size', sa.Integer),
        sa.Column('armed', sa.Boolean)
    )
    op.create_table(
        'officers',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('ship_id', sa.Integer),
        sa.Column('first_name', sa.String),
        sa.Column('last_name', sa.String),
        sa.Column('rank', sa.String)
    )


def downgrade() -> None:
    op.drop_table('ships')
    op.drop_table('officers')
