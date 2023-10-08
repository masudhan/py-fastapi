"""add content column in posts table

Revision ID: 7c7c76b5ac6f
Revises: 046c508f5fa2
Create Date: 2023-10-08 21:32:18.242159

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7c7c76b5ac6f'
down_revision: Union[str, None] = '046c508f5fa2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
