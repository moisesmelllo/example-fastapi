"""add last few columns to post table

Revision ID: 47060dfc7795
Revises: a353f8b7488f
Create Date: 2023-02-25 16:32:36.074987

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '47060dfc7795'
down_revision = 'a353f8b7488f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),
    )
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
