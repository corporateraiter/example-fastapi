"""add foreign key to posts table

Revision ID: 1af705f333a0
Revises: 1261170accdf
Create Date: 2022-04-07 08:56:35.795249

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1af705f333a0'
down_revision = '1261170accdf'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer())) #couldn't place nullable in here for some reason
    op.create_foreign_key('posts_users_fk', source_table='posts', referent_table='users', 
    local_cols=['owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('posts_users_fk', table_name='posts')
    op.drop_column('posts', column_name='owner_id')

    pass
