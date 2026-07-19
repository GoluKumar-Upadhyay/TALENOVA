"""LMS course migration: add new fields to courses + create module/submodule/batch/application tables."""

from alembic import op
import sqlalchemy as sa

revision = "0018_courses_lms"
down_revision = "0016_missing_core_tables"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ── New columns on courses ─────────────────────────────────────────────
    with op.batch_alter_table("courses") as batch:
        batch.add_column(sa.Column("level", sa.String(50), nullable=True))
        batch.add_column(sa.Column("price", sa.Numeric(10, 2), nullable=True))
        batch.add_column(sa.Column("certificate_available", sa.Boolean(), nullable=False, server_default="false"))
        batch.add_column(sa.Column("skills_covered", sa.JSON(), nullable=False, server_default="[]"))
        batch.add_column(sa.Column("technologies", sa.JSON(), nullable=False, server_default="[]"))
        batch.add_column(sa.Column("learning_outcomes", sa.JSON(), nullable=False, server_default="[]"))
        batch.add_column(sa.Column("career_opportunities", sa.JSON(), nullable=False, server_default="[]"))
        batch.add_column(sa.Column("faqs", sa.JSON(), nullable=False, server_default="[]"))

    # ── course_modules ─────────────────────────────────────────────────────
    op.create_table(
        "course_modules",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("uuid", sa.String(36), nullable=False, unique=True),
        sa.Column("course_id", sa.Integer(), sa.ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("position", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_course_modules_course_pos", "course_modules", ["course_id", "position"])

    # ── course_submodules ──────────────────────────────────────────────────
    op.create_table(
        "course_submodules",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("uuid", sa.String(36), nullable=False, unique=True),
        sa.Column("module_id", sa.Integer(), sa.ForeignKey("course_modules.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("position", sa.Integer(), nullable=False, server_default="0"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_index("ix_course_submodules_mod_pos", "course_submodules", ["module_id", "position"])

    # ── course_batches ─────────────────────────────────────────────────────
    op.create_table(
        "course_batches",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("uuid", sa.String(36), nullable=False, unique=True),
        sa.Column("course_id", sa.Integer(), sa.ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("start_date", sa.Date(), nullable=True),
        sa.Column("end_date", sa.Date(), nullable=True),
        sa.Column("application_deadline", sa.Date(), nullable=True),
        sa.Column("max_seats", sa.Integer(), nullable=True),
        sa.Column("remaining_seats", sa.Integer(), nullable=True),
        sa.Column("time_slot", sa.String(50), nullable=True),
        sa.Column("status", sa.String(50), nullable=False, server_default="draft"),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )

    # ── course_applications ────────────────────────────────────────────────
    op.create_table(
        "course_applications",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("uuid", sa.String(36), nullable=False, unique=True),
        sa.Column("course_id", sa.Integer(), sa.ForeignKey("courses.id", ondelete="CASCADE"), nullable=False, index=True),
        sa.Column("batch_id", sa.Integer(), sa.ForeignKey("course_batches.id", ondelete="SET NULL"), nullable=True),
        sa.Column("full_name", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), nullable=False, index=True),
        sa.Column("phone", sa.String(30), nullable=True),
        sa.Column("college", sa.String(255), nullable=True),
        sa.Column("degree", sa.String(255), nullable=True),
        sa.Column("current_year", sa.String(50), nullable=True),
        sa.Column("linkedin_url", sa.String(1000), nullable=True),
        sa.Column("github_url", sa.String(1000), nullable=True),
        sa.Column("motivation", sa.Text(), nullable=True),
        sa.Column("resume_url", sa.String(1000), nullable=True),
        sa.Column("status", sa.String(30), nullable=False, server_default="pending"),
        sa.Column("admin_notes", sa.Text(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    op.drop_table("course_applications")
    op.drop_table("course_batches")
    op.drop_index("ix_course_submodules_mod_pos", "course_submodules")
    op.drop_table("course_submodules")
    op.drop_index("ix_course_modules_course_pos", "course_modules")
    op.drop_table("course_modules")
    with op.batch_alter_table("courses") as batch:
        for col in ("faqs", "career_opportunities", "learning_outcomes", "technologies",
                    "skills_covered", "certificate_available", "price", "level"):
            batch.drop_column(col)
