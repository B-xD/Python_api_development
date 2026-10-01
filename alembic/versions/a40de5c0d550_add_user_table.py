"""add user table

Revision ID: a40de5c0d550
Revises: ecb17994bbfe
Create Date: 2026-09-30 19:49:57.429871

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a40de5c0d550'
down_revision: Union[str, Sequence[str], None] = 'ecb17994bbfe'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('users', 
                    sa.Column('id', sa.Integer(), nullable= False),
                    sa.Column('email', sa.String(), nullable= False),
                    sa.Column('password', sa.String(), nullable= False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text("now()"), nullable= False),
                              sa.PrimaryKeyConstraint("id"),
                              sa.UniqueConstraint('email')
                    )
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('users')

    pass
