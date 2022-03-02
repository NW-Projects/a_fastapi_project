"""votes table

Revision ID: 268205b0c902
Revises: 688e4f508de8
Create Date: 2022-03-02 10:39:18.811277

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '268205b0c902'
down_revision = '688e4f508de8'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('votes',
                        sa.Column('user_id', sa.Integer(), nullable=False),
                        sa.Column('post_id', sa.Integer(), nullable=False),
                        sa.ForeignKeyConstraint(['post_id'], ['posts.id'], ondelete='CASCADE'),
                        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
                        sa.PrimaryKeyConstraint('user_id', 'post_id'))
    pass


def downgrade():
    op.drop_table('votes')
    pass
