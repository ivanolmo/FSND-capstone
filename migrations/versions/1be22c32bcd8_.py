"""empty message

Revision ID: 1be22c32bcd8
Revises: 29656a503df2
Create Date: 2020-02-20 18:06:32.042826

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1be22c32bcd8'
down_revision = '29656a503df2'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('players', sa.Column('salary', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('players', 'salary')
    # ### end Alembic commands ###