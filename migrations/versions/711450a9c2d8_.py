"""empty message

Revision ID: 711450a9c2d8
Revises: d3863285b00c
Create Date: 2022-11-08 13:46:01.486400

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '711450a9c2d8'
down_revision = 'd3863285b00c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('product_name_key', 'product', type_='unique')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('product_name_key', 'product', ['name'])
    # ### end Alembic commands ###