"""add a new column to posts table

Revision ID: ecb17994bbfe
Revises: f69b9dc2e82a
Create Date: 2026-09-30 19:02:40.242814

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ecb17994bbfe'
down_revision: Union[str, Sequence[str], None] = 'f69b9dc2e82a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('content', sa.String(), nullable = False))
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts', 'content')
    pass

#run alembic upgrade f69b9dc2e82a