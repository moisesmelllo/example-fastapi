"""create posts table

Revision ID: 08ec537e9f1e
Revises: 
Create Date: 2023-02-25 15:47:12.268687

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '08ec537e9f1e'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
                    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
