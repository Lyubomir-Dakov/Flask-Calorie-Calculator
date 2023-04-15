"""add updated_on and deleted_on columns on UserModel

Revision ID: b3aa1a7cbeaf
Revises: 027a1555bb03
Create Date: 2023-04-15 10:26:04.306256

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b3aa1a7cbeaf'
down_revision = '027a1555bb03'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('admins', sa.Column('updated_on', sa.DateTime(), nullable=True))
    op.add_column('staffs', sa.Column('updated_on', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('deleted_on', sa.DateTime(), nullable=True))
    op.add_column('users', sa.Column('updated_on', sa.DateTime(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('users', 'updated_on')
    op.drop_column('users', 'deleted_on')
    op.drop_column('staffs', 'updated_on')
    op.drop_column('admins', 'updated_on')
    # ### end Alembic commands ###