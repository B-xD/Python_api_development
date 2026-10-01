"""add a few more columns to posts table

Revision ID: 60bbddc12eac
Revises: ff61335af361
Create Date: 2026-09-30 20:51:57.591139

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '60bbddc12eac'
down_revision: Union[str, Sequence[str], None] = 'ff61335af361'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# published = Column(Boolean, server_default = 'True', nullable = False)
# created_at = Column(TIMESTAMP(timezone=True), server_default=text('NOW()'), nullable=False)

   
def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('published', sa.Boolean(), server_default = 'True', nullable=False))

    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                                         server_default=sa.text('now()'), nullable= False)
                                         )
    pass



def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('posts','published')
    op.drop_column('posts', 'created_at')
    
    pass
