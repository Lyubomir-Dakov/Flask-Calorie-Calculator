"""corrections on SubscriptionModel

Revision ID: f85bedb320ac
Revises: 449e51f336a1
Create Date: 2023-04-16 10:06:15.915261

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f85bedb320ac'
down_revision = '449e51f336a1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('subscriptions',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('paypal_id', sa.String(), nullable=False),
    sa.Column('title', sa.String(), nullable=False),
    sa.Column('status', sa.Enum('active', 'paused', 'canceled', name='subscriptionstatus'), nullable=False),
    sa.Column('created_on', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_on', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('initial_tax', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('monthly_tax', sa.Numeric(precision=10, scale=2), nullable=False),
    sa.Column('subscriber_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['subscriber_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('subscriptions')
    # ### end Alembic commands ###
