"""create posts table

Revision ID: 2a27351e9ff0
Revises: 
Create Date: 2023-04-25 21:54:03.935640

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2a27351e9ff0'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # op.create_table('posts', 
    #                 sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
    #                 sa.Column('title', sa.String(), nullable=False)
    #                 )
    pass


def downgrade() -> None:
    # op.drop_table('posts')
    pass
