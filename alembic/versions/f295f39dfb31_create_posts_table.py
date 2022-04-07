"""create posts table

Revision ID: f295f39dfb31
Revises: 
Create Date: 2022-04-06 23:28:43.395049

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f295f39dfb31'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
    sa.Column('title', sa.String(), nullable=False))


def downgrade():
    op.drop_table('posts')
    pass
