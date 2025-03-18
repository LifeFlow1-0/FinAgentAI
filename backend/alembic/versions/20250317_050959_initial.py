"""initial

Revision ID: 4df87650d6a3
Revises: 
Create Date: 2025-03-17 05:09:59.394648+00:00

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "4df87650d6a3"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(), nullable=False),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email')
    )

    # Create plaid_items table
    op.create_table(
        'plaid_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('item_id', sa.String(), nullable=False),
        sa.Column('access_token', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('item_id')
    )

    # Create plaid_accounts table
    op.create_table(
        'plaid_accounts',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('plaid_item_id', sa.Integer(), nullable=False),
        sa.Column('account_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('subtype', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['plaid_item_id'], ['plaid_items.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('account_id')
    )

    # Create transactions table
    op.create_table(
        'transactions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('plaid_item_id', sa.Integer(), nullable=False),
        sa.Column('plaid_account_id', sa.Integer(), nullable=False),
        sa.Column('amount', sa.Float(), nullable=False),
        sa.Column('currency', sa.String(), nullable=False),
        sa.Column('type', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=True),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('merchant_name', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('transaction_date', sa.Date(), nullable=False),
        sa.Column('posted_date', sa.Date(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['plaid_account_id'], ['plaid_accounts.id'], ),
        sa.ForeignKeyConstraint(['plaid_item_id'], ['plaid_items.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create personality_profiles table
    op.create_table(
        'personality_profiles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('openness', sa.String(), nullable=False),
        sa.Column('social_energy', sa.String(), nullable=False),
        sa.Column('learning_style', sa.String(), nullable=False),
        sa.Column('activity_intensity', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )


def downgrade() -> None:
    op.drop_table('personality_profiles')
    op.drop_table('transactions')
    op.drop_table('plaid_accounts')
    op.drop_table('plaid_items')
    op.drop_table('users')
