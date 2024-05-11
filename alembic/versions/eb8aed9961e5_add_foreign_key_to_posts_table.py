"""add foreign key to posts table

Revision ID: eb8aed9961e5
Revises: 6e27a626ebb3
Create Date: 2024-05-10 20:09:24.448073

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'eb8aed9961e5'
down_revision: Union[str, None] = '6e27a626ebb3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id',sa.Integer(),sa.ForeignKey('users.id',ondelete='CASCADE'),nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts','owner_id')
    pass
