"""add last few columns to posts table

Revision ID: 98b498333e3e
Revises: eb8aed9961e5
Create Date: 2024-05-10 20:21:21.937052

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '98b498333e3e'
down_revision: Union[str, None] = 'eb8aed9961e5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('published',sa.Boolean(),server_default='False',nullable=False))
    op.add_column('posts',sa.Column('rating',sa.Integer(),server_default='0',nullable=False))
    op.add_column('posts',sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False))
                        
    pass


def downgrade() -> None:
    op.drop_column('posts','published')
    op.drop_column('posts','rating')
    op.drop_column('posts','created_at')
    pass
