"""create ai runs table

Revision ID: 0002_create_ai_runs
Revises: 0001_create_users
Create Date: 2026-08-08
"""
from alembic import op
import sqlalchemy as sa

revision = "0002_create_ai_runs"
down_revision = "0001_create_users"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "ai_runs",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("provider", sa.String(length=50), nullable=False),
        sa.Column("model", sa.String(length=100), nullable=False),
        sa.Column("prompt", sa.Text(), nullable=False),
        sa.Column("output", sa.Text(), nullable=False),
        sa.Column("status", sa.String(length=30), nullable=False, server_default="completed"),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_ai_runs_user_id", "ai_runs", ["user_id"])


def downgrade() -> None:
    op.drop_index("ix_ai_runs_user_id", table_name="ai_runs")
    op.drop_table("ai_runs")
