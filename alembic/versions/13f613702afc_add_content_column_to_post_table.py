"""add content column to post table

Revision ID: 13f613702afc
Revises: 20f1f1ad756d
Create Date: 2023-04-27 22:09:06.517956

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13f613702afc'
down_revision = '20f1f1ad756d'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', 
                  sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts',
                   'content')
    pass
