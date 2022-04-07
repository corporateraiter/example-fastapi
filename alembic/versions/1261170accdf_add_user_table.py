"""add user table

Revision ID: 1261170accdf
Revises: ad4bd5f07063
Create Date: 2022-04-06 23:59:03.423051

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1261170accdf'
down_revision = 'ad4bd5f07063'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
            sa.Column('id', sa.Integer(), nullable=False),
            sa.Column('email', sa.String(), nullable=False),
            sa.Column('password', sa.String(), nullable=False),
            sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                server_default=sa.text('now()'), nullable= False),
            sa.PrimaryKeyConstraint('id'),
            sa.UniqueConstraint('email')
            )
    pass


def downgrade():
    op.drop_table('users')
    pass
