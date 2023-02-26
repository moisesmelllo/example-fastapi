"""add content column to post table

Revision ID: 528f0c2d36a7
Revises: 08ec537e9f1e
Create Date: 2023-02-25 16:04:03.245739

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '528f0c2d36a7'
down_revision = '08ec537e9f1e'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
