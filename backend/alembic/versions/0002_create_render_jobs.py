"""create render_jobs table

Revision ID: 0002_render_jobs
Revises: 0001_initial
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = "0002_render_jobs"
down_revision = "0001_initial"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "render_jobs",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("progress", sa.Integer(), nullable=False),
        sa.Column("output_path", sa.Text(), nullable=True),
        sa.Column("error", sa.Text(), nullable=True),
        sa.Column("celery_task_id", sa.String(length=255), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("started_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("completed_at", sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_render_jobs_status", "render_jobs", ["status"], unique=False)
    op.create_index("ix_render_jobs_celery_task_id", "render_jobs", ["celery_task_id"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_render_jobs_celery_task_id", table_name="render_jobs")
    op.drop_index("ix_render_jobs_status", table_name="render_jobs")
    op.drop_table("render_jobs")
