"""create subscription model

Revision ID: dfa7d37b7ec7
Revises: 99daa40e1d1a
Create Date: 2023-04-15 20:32:42.171794

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dfa7d37b7ec7'
down_revision = '99daa40e1d1a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subscriptions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('paypal_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=False, server_default='Premium membership'),
    sa.Column('status', sa.Enum('active', 'paused', 'canceled', name='subscriptionstatus'), nullable=False, default='active'),
    sa.Column('created_on', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_on', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('initial_tax', sa.Numeric(precision=10, scale=2), nullable=False, server_default='3'),
    sa.Column('monthly_tax', sa.Numeric(precision=10, scale=2), nullable=False, server_default='5'),
    sa.Column('subscriber_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['subscriber_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###



def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('subscriptions')
    # ### end Alembic commands ###
