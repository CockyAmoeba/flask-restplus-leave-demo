"""empty message

Revision ID: 454530f60ccf
Revises: 36e0bc3977fc
Create Date: 2017-03-27 08:31:55.023335

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '454530f60ccf'
down_revision = '36e0bc3977fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('leave',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('start_date', sa.DateTime(), nullable=True),
    sa.Column('end_date', sa.DateTime(), nullable=True),
    sa.Column('days_of_leave', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=8), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('leave')
    # ### end Alembic commands ###