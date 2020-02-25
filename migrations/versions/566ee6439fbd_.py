"""empty message

Revision ID: 566ee6439fbd
Revises: 1be22c32bcd8
Create Date: 2020-02-23 21:15:15.212373

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '566ee6439fbd'
down_revision = '1be22c32bcd8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('teams', sa.Column('team_city', sa.String(), nullable=True))
    op.add_column('teams', sa.Column('team_state', sa.String(), nullable=True))
    op.drop_column('teams', 'state')
    op.drop_column('teams', 'city')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('teams', sa.Column('city', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('teams', sa.Column('state', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_column('teams', 'team_state')
    op.drop_column('teams', 'team_city')
    # ### end Alembic commands ###
