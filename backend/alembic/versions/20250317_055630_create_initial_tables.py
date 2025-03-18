"""create initial tables

Revision ID: acbe325641f2
Revises: 4df87650d6a3
Create Date: 2025-03-17 05:56:30.518890+00:00

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "acbe325641f2"
down_revision = "4df87650d6a3"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_index(
        op.f("ix_personality_profiles_id"),
        "personality_profiles",
        ["id"],
        unique=False,
    )
    op.add_column(
        "plaid_accounts",
        sa.Column("official_name", sa.String(), nullable=True),
    )
    op.add_column(
        "plaid_accounts", sa.Column("mask", sa.String(), nullable=True)
    )
    op.alter_column(
        "plaid_accounts",
        "plaid_item_id",
        existing_type=sa.INTEGER(),
        nullable=True,
    )
    op.alter_column(
        "plaid_accounts",
        "account_id",
        existing_type=sa.VARCHAR(),
        nullable=True,
    )
    op.alter_column(
        "plaid_accounts", "name", existing_type=sa.VARCHAR(), nullable=True
    )
    op.alter_column(
        "plaid_accounts", "type", existing_type=sa.VARCHAR(), nullable=True
    )
    op.alter_column(
        "plaid_accounts",
        "created_at",
        existing_type=sa.DATETIME(),
        nullable=True,
    )
    op.alter_column(
        "plaid_accounts",
        "updated_at",
        existing_type=sa.DATETIME(),
        nullable=True,
    )
    op.create_index(
        op.f("ix_plaid_accounts_account_id"),
        "plaid_accounts",
        ["account_id"],
        unique=True,
    )
    op.create_index(
        op.f("ix_plaid_accounts_id"), "plaid_accounts", ["id"], unique=False
    )
    op.add_column(
        "plaid_items", sa.Column("institution_id", sa.String(), nullable=True)
    )
    op.add_column(
        "plaid_items",
        sa.Column("institution_name", sa.String(), nullable=True),
    )
    op.alter_column(
        "plaid_items", "item_id", existing_type=sa.VARCHAR(), nullable=True
    )
    op.alter_column(
        "plaid_items",
        "access_token",
        existing_type=sa.VARCHAR(),
        nullable=True,
    )
    op.alter_column(
        "plaid_items", "created_at", existing_type=sa.DATETIME(), nullable=True
    )
    op.alter_column(
        "plaid_items", "updated_at", existing_type=sa.DATETIME(), nullable=True
    )
    op.create_index(
        op.f("ix_plaid_items_id"), "plaid_items", ["id"], unique=False
    )
    op.create_index(
        op.f("ix_plaid_items_item_id"), "plaid_items", ["item_id"], unique=True
    )
    op.create_unique_constraint(None, "plaid_items", ["access_token"])
    op.drop_constraint(None, "plaid_items", type_="foreignkey")
    op.drop_column("plaid_items", "user_id")
    op.alter_column(
        "transactions", "type", existing_type=sa.VARCHAR(), nullable=False
    )
    op.alter_column(
        "transactions", "category", existing_type=sa.VARCHAR(), nullable=False
    )
    op.alter_column(
        "transactions", "status", existing_type=sa.VARCHAR(), nullable=False
    )
    op.alter_column(
        "transactions",
        "transaction_date",
        existing_type=sa.DATE(),
        type_=sa.DateTime(),
        existing_nullable=False,
    )
    op.alter_column(
        "transactions",
        "posted_date",
        existing_type=sa.DATE(),
        type_=sa.DateTime(),
        nullable=False,
    )
    op.create_index(
        op.f("ix_transactions_id"), "transactions", ["id"], unique=False
    )
    op.create_index(
        "ix_transactions_plaid_account_id",
        "transactions",
        ["plaid_account_id"],
        unique=False,
    )
    op.create_index(
        "ix_transactions_status", "transactions", ["status"], unique=False
    )
    op.create_index(
        "ix_transactions_transaction_date",
        "transactions",
        ["transaction_date"],
        unique=False,
    )
    op.create_index(
        "ix_transactions_user_id", "transactions", ["user_id"], unique=False
    )
    op.alter_column(
        "users", "created_at", existing_type=sa.DATETIME(), nullable=True
    )
    op.alter_column(
        "users", "updated_at", existing_type=sa.DATETIME(), nullable=True
    )
    op.create_index(op.f("ix_users_email"), "users", ["email"], unique=True)
    op.create_index(op.f("ix_users_id"), "users", ["id"], unique=False)
    op.drop_column("users", "is_active")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "users", sa.Column("is_active", sa.BOOLEAN(), nullable=False)
    )
    op.drop_index(op.f("ix_users_id"), table_name="users")
    op.drop_index(op.f("ix_users_email"), table_name="users")
    op.alter_column(
        "users", "updated_at", existing_type=sa.DATETIME(), nullable=False
    )
    op.alter_column(
        "users", "created_at", existing_type=sa.DATETIME(), nullable=False
    )
    op.drop_index("ix_transactions_user_id", table_name="transactions")
    op.drop_index(
        "ix_transactions_transaction_date", table_name="transactions"
    )
    op.drop_index("ix_transactions_status", table_name="transactions")
    op.drop_index(
        "ix_transactions_plaid_account_id", table_name="transactions"
    )
    op.drop_index(op.f("ix_transactions_id"), table_name="transactions")
    op.alter_column(
        "transactions",
        "posted_date",
        existing_type=sa.DateTime(),
        type_=sa.DATE(),
        nullable=True,
    )
    op.alter_column(
        "transactions",
        "transaction_date",
        existing_type=sa.DateTime(),
        type_=sa.DATE(),
        existing_nullable=False,
    )
    op.alter_column(
        "transactions", "status", existing_type=sa.VARCHAR(), nullable=True
    )
    op.alter_column(
        "transactions", "category", existing_type=sa.VARCHAR(), nullable=True
    )
    op.alter_column(
        "transactions", "type", existing_type=sa.VARCHAR(), nullable=True
    )
    op.add_column(
        "plaid_items", sa.Column("user_id", sa.INTEGER(), nullable=False)
    )
    op.create_foreign_key(None, "plaid_items", "users", ["user_id"], ["id"])
    op.drop_constraint(None, "plaid_items", type_="unique")
    op.drop_index(op.f("ix_plaid_items_item_id"), table_name="plaid_items")
    op.drop_index(op.f("ix_plaid_items_id"), table_name="plaid_items")
    op.alter_column(
        "plaid_items",
        "updated_at",
        existing_type=sa.DATETIME(),
        nullable=False,
    )
    op.alter_column(
        "plaid_items",
        "created_at",
        existing_type=sa.DATETIME(),
        nullable=False,
    )
    op.alter_column(
        "plaid_items",
        "access_token",
        existing_type=sa.VARCHAR(),
        nullable=False,
    )
    op.alter_column(
        "plaid_items", "item_id", existing_type=sa.VARCHAR(), nullable=False
    )
    op.drop_column("plaid_items", "institution_name")
    op.drop_column("plaid_items", "institution_id")
    op.drop_index(op.f("ix_plaid_accounts_id"), table_name="plaid_accounts")
    op.drop_index(
        op.f("ix_plaid_accounts_account_id"), table_name="plaid_accounts"
    )
    op.alter_column(
        "plaid_accounts",
        "updated_at",
        existing_type=sa.DATETIME(),
        nullable=False,
    )
    op.alter_column(
        "plaid_accounts",
        "created_at",
        existing_type=sa.DATETIME(),
        nullable=False,
    )
    op.alter_column(
        "plaid_accounts", "type", existing_type=sa.VARCHAR(), nullable=False
    )
    op.alter_column(
        "plaid_accounts", "name", existing_type=sa.VARCHAR(), nullable=False
    )
    op.alter_column(
        "plaid_accounts",
        "account_id",
        existing_type=sa.VARCHAR(),
        nullable=False,
    )
    op.alter_column(
        "plaid_accounts",
        "plaid_item_id",
        existing_type=sa.INTEGER(),
        nullable=False,
    )
    op.drop_column("plaid_accounts", "mask")
    op.drop_column("plaid_accounts", "official_name")
    op.drop_index(
        op.f("ix_personality_profiles_id"), table_name="personality_profiles"
    )
    # ### end Alembic commands ###
