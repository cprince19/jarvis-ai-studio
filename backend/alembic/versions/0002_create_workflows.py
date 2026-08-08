"""create workflows table

Revision ID: 0002_create_workflows
Revises: 0001_create_users
Create Date: 2026-08-08
"""
from alembic import op
import sqlalchemy as sa

revision = "0002_create_workflows"
down_revision = "0001_create_users"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "workflows",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("owner_id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="draft"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["owner_id"], ["users.id"], ondelete="CASCADE"),
    )
    op.create_index("ix_workflows_owner_id", "workflows", ["owner_id"])


def downgrade() -> None:
    op.drop_index("ix_workflows_owner_id", table_name="workflows")
    op.drop_table("workflows")
