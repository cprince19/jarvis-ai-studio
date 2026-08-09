"""create YouTube projects

Revision ID: 0004_create_youtube_projects
Revises: 0003_create_conversations
"""
from alembic import op
import sqlalchemy as sa

revision = "0004_create_youtube_projects"
down_revision = "0003_create_conversations"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "youtube_projects",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("user_id", sa.Integer(), sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("topic", sa.String(length=500), nullable=False),
        sa.Column("audience", sa.String(length=200), nullable=False),
        sa.Column("language", sa.String(length=50), nullable=False),
        sa.Column("tone", sa.String(length=100), nullable=False),
        sa.Column("provider", sa.String(length=50), nullable=False),
        sa.Column("model", sa.String(length=100), nullable=True),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("research", sa.Text(), nullable=True),
        sa.Column("script", sa.Text(), nullable=True),
        sa.Column("title", sa.String(length=500), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("tags", sa.Text(), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
    )
    op.create_index("ix_youtube_projects_user_id", "youtube_projects", ["user_id"])
    op.create_index("ix_youtube_projects_status", "youtube_projects", ["status"])


def downgrade() -> None:
    op.drop_index("ix_youtube_projects_status", table_name="youtube_projects")
    op.drop_index("ix_youtube_projects_user_id", table_name="youtube_projects")
    op.drop_table("youtube_projects")
