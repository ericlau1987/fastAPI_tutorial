"""add last few columns

Revision ID: bc07b52d53b6
Revises: 256d9e443b20
Create Date: 2023-04-27 22:31:16.709497

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bc07b52d53b6'
down_revision = '256d9e443b20'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'posts', sa.Column(
            'published', sa.Boolean(), nullable=False, server_default='True'),
        )
    op.add_column(
        'posts',  sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              server_default=sa.text('now()'), nullable=False)
    )
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
