"""add foreign-key to post table

Revision ID: 256d9e443b20
Revises: 336ad2a7a3af
Create Date: 2023-04-27 22:24:04.118158

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '256d9e443b20'
down_revision = '336ad2a7a3af'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts',sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts",
                          referent_table="users",
                          local_cols=['owner_id'],
                          remote_cols=["id"])
                  
    
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
