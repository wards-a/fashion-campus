"""empty message

Revision ID: d3863285b00c
Revises: 5ec3f48138f7
Create Date: 2022-11-07 12:46:15.577649

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'd3863285b00c'
down_revision = '5ec3f48138f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('product_category_id_fkey', 'product', type_='foreignkey')
    op.create_foreign_key(None, 'product', 'category', ['category_id'], ['id'], ondelete='SET NULL')
    op.drop_column('product_image', 'updated_at')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product_image', sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'product', type_='foreignkey')
    op.create_foreign_key('product_category_id_fkey', 'product', 'category', ['category_id'], ['id'])
    # ### end Alembic commands ###
