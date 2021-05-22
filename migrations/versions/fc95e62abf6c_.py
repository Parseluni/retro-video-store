"""empty message

Revision ID: fc95e62abf6c
Revises: 7c4c3ed70f15
Create Date: 2021-05-21 16:51:24.725329

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fc95e62abf6c'
down_revision = '7c4c3ed70f15'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('videos', 'available_inventory',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('videos', 'available_inventory',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
