"""add content column to posts table

Revision ID: ad4bd5f07063
Revises: f295f39dfb31
Create Date: 2022-04-06 23:47:35.658521

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ad4bd5f07063'
down_revision = 'f295f39dfb31'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column("content", sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
