"""Change ingredients column to JSON type

Revision ID: csb4f58ghee6
Revises: c3b4d58baee6
Create Date: 2023-04-19 20:15:57.225360

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'csb4f58ghee6'
down_revision = 'c3b4d58baee6'
branch_labels = None
depends_on = None


def upgrade():
    op.alter_column('recipes', 'ingredients', type_=sa.JSON(), postgresql_using='ingredients::json')


def downgrade():
    op.alter_column('recipes', 'ingredients', type_=sa.Text(), postgresql_using='ingredients::text')
