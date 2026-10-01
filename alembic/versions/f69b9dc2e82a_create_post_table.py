"""create post table

Revision ID: f69b9dc2e82a
Revises: 
Create Date: 2026-09-30 18:39:25.644435

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f69b9dc2e82a'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

#runs the commands for the changes we want to make
def upgrade() -> None:
    """Upgrade schema."""

    op.create_table('posts', sa.Column('id', sa.Integer(), nullable = False, primary_key= True ),
                    sa.Column('title', sa.String(), nullable=False)
                    )
    pass

#rollback 
def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table('posts')

    pass
