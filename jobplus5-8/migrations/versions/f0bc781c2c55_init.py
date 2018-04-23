"""init

Revision ID: f0bc781c2c55
Revises: 94d5aea1b02e
Create Date: 2018-04-19 22:13:33.468223

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'f0bc781c2c55'
down_revision = '94d5aea1b02e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('job', sa.Column('online', sa.Boolean(), nullable=True))
    op.drop_column('job', 'is_online')
    op.add_column('user', sa.Column('enabled', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'enabled')
    op.add_column('job', sa.Column('is_online', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.drop_column('job', 'online')
    # ### end Alembic commands ###