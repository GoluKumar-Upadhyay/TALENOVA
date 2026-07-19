"""Initial TALENOVA schema.

Revision ID: 0001_initial_auth_and_cms
Revises:
Create Date: 2026-07-18
"""

from alembic import op
import sqlalchemy as sa

revision = "0001_initial_auth_and_cms"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create leadership profiles table for founder and co-founder CMS data."""

    op.create_table(
        "founders",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("uuid", sa.String(length=36), nullable=False, unique=True),
        sa.Column("founder_type", sa.String(length=20), nullable=False, unique=True),
        sa.Column("name", sa.String(length=180), nullable=False),
        sa.Column("bio", sa.Text(), nullable=True),
        sa.Column("photo_url", sa.String(length=1000), nullable=True),
        sa.Column("education", sa.JSON(), nullable=False),
        sa.Column("experience", sa.JSON(), nullable=False),
        sa.Column("research", sa.JSON(), nullable=False),
        sa.Column("achievements", sa.JSON(), nullable=False),
        sa.Column("social_links", sa.JSON(), nullable=False),
        sa.Column("resume_url", sa.String(length=1000), nullable=True),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    """Remove founder leadership profiles."""

    op.drop_table("founders")
