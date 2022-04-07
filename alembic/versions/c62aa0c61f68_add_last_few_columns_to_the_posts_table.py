"""add last few columns to the posts table

Revision ID: c62aa0c61f68
Revises: 1af705f333a0
Create Date: 2022-04-07 10:09:30.469456

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c62aa0c61f68'
down_revision = '1af705f333a0'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(),
    nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(), nullable=False,
    server_default=sa.text('now()')),)
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')

    pass
