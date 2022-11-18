"""empty message

Revision ID: e1fb6f00d762
Revises: 711450a9c2d8
Create Date: 2022-11-08 14:10:47.887082

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e1fb6f00d762'
down_revision = '711450a9c2d8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('product', 'description',
               existing_type=sa.TEXT(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('product', 'description',
               existing_type=sa.TEXT(),
               nullable=False)
    # ### end Alembic commands ###