"""add foreign_key to posts table

Revision ID: ff61335af361
Revises: a40de5c0d550
Create Date: 2026-09-30 20:40:38.370680

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ff61335af361'
down_revision: Union[str, Sequence[str], None] = 'a40de5c0d550'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable= False))
    op.create_foreign_key("posts_users_fk", source_table= "posts", 
                          referent_table='users', 
                          local_cols= ['owner_id'], 
                          remote_cols=['id'], 
                          ondelete= "CASCADE")
    pass


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', 'owner_id')
    
    pass
