"""create posts tables

Revision ID: 20f1f1ad756d
Revises: 2a27351e9ff0
Create Date: 2023-04-27 22:02:20.994822

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '20f1f1ad756d'
down_revision = '2a27351e9ff0'
branch_labels = None
depends_on = None


def upgrade() -> None:
  op.create_table('posts', 
                    sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False)
                    )
  pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
