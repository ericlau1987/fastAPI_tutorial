"""add user tables

Revision ID: 336ad2a7a3af
Revises: 13f613702afc
Create Date: 2023-04-27 22:16:30.219880

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '336ad2a7a3af'
down_revision = '13f613702afc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password',sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )
    pass


def downgrade() -> None:
    op.drop_table('users')
    pass
