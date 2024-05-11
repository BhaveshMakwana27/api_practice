"""create user table

Revision ID: 6e27a626ebb3
Revises: c4b475ea4a6d
Create Date: 2024-05-10 19:15:12.561226

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6e27a626ebb3'
down_revision: Union[str, None] = 'c4b475ea4a6d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table('users',sa.Column('id',sa.Integer(),nullable=False),
                            sa.Column('email',sa.String(),nullable=False),
                            sa.Column('password',sa.String(),nullable=False),
                            sa.Column('created_at',sa.TIMESTAMP(timezone=True),server_default=sa.text('now()'),nullable=False),
                            sa.PrimaryKeyConstraint('id'),
                            sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
