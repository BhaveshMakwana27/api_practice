"""add contact column

Revision ID: c4b475ea4a6d
Revises: 06d7e9b0fc91
Create Date: 2024-05-10 19:07:59.104646

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c4b475ea4a6d'
down_revision: Union[str, None] = '06d7e9b0fc91'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('content',sa.String(),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','content')
    pass
