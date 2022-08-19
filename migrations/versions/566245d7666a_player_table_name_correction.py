"""player table name correction

Revision ID: 566245d7666a
Revises: 817d0612de7d
Create Date: 2022-08-18 13:13:52.755088

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '566245d7666a'
down_revision = '817d0612de7d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('player',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('playername', sa.String(length=120), nullable=True),
    sa.Column('position', sa.String(length=5), nullable=True),
    sa.Column('value', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_player_playername'), 'player', ['playername'], unique=True)
    op.create_index(op.f('ix_player_position'), 'player', ['position'], unique=False)
    op.drop_index('ix_players_playername', table_name='players')
    op.drop_index('ix_players_position', table_name='players')
    op.drop_table('players')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('players',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('playername', sa.VARCHAR(length=120), nullable=True),
    sa.Column('position', sa.VARCHAR(length=5), nullable=True),
    sa.Column('value', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index('ix_players_position', 'players', ['position'], unique=False)
    op.create_index('ix_players_playername', 'players', ['playername'], unique=False)
    op.drop_index(op.f('ix_player_position'), table_name='player')
    op.drop_index(op.f('ix_player_playername'), table_name='player')
    op.drop_table('player')
    # ### end Alembic commands ###
