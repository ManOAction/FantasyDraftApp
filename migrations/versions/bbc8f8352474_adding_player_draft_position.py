"""adding player draft position

Revision ID: bbc8f8352474
Revises: 9bba1a7999bc
Create Date: 2022-08-24 17:56:14.325321

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bbc8f8352474'
down_revision = '9bba1a7999bc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('player', sa.Column('draft_pick', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('player', 'draft_pick')
    # ### end Alembic commands ###
