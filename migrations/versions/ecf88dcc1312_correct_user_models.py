"""correct user models

Revision ID: ecf88dcc1312
Revises: csb4f58ghee6
Create Date: 2023-04-20 08:13:12.061743

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ecf88dcc1312'
down_revision = 'csb4f58ghee6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('admins', sa.Column('deleted', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('admins', 'deleted')
    # ### end Alembic commands ###
