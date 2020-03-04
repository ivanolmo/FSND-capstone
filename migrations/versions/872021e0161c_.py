"""empty message

Revision ID: 872021e0161c
Revises: 70e4df4b4f4c
Create Date: 2020-03-04 13:35:26.370000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '872021e0161c'
down_revision = '70e4df4b4f4c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('teams', sa.Column('abbr', sa.String(), nullable=True))
    op.add_column('teams', sa.Column('city', sa.String(), nullable=True))
    op.add_column('teams', sa.Column('name', sa.String(), nullable=True))
    op.add_column('teams', sa.Column('state', sa.String(), nullable=True))
    op.drop_column('teams', 'team_short')
    op.drop_column('teams', 'team_state')
    op.drop_column('teams', 'team_city')
    op.drop_column('teams', 'team_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('teams', sa.Column('team_name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('teams', sa.Column('team_city', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('teams', sa.Column('team_state', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('teams', sa.Column('team_short', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('teams', 'state')
    op.drop_column('teams', 'name')
    op.drop_column('teams', 'city')
    op.drop_column('teams', 'abbr')
    # ### end Alembic commands ###