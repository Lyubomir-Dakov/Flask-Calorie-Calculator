"""make corrections on SubscriptionModel

Revision ID: 449e51f336a1
Revises: dfa7d37b7ec7
Create Date: 2023-04-16 09:41:23.597393

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '449e51f336a1'
down_revision = 'dfa7d37b7ec7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subscriptions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('paypal_id', sa.String(), nullable=False),
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