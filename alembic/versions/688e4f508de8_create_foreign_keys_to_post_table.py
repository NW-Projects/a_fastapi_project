"""create foreign keys to post table

Revision ID: 688e4f508de8
Revises: d5001efe8ff2
Create Date: 2022-03-02 10:29:44.425219

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '688e4f508de8'
down_revision = 'd5001efe8ff2'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users", local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete="CASCADE")

    pass


def downgrade():
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
