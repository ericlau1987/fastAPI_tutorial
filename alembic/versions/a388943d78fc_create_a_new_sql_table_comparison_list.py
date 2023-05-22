"""create a new sql table comparison list

Revision ID: a388943d78fc
Revises: c397e4ca4ffc
Create Date: 2023-05-22 21:26:51.543081

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a388943d78fc'
down_revision = 'c397e4ca4ffc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('user_id', sa.String(), nullable=False),
                    sa.Column('place_id',sa.String(), nullable=False),
                    sa.Column('address',sa.String(), nullable=False),
                    sa.Column('image_url',sa.String(), nullable=True),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('id')
                    )


def downgrade() -> None:
    pass
