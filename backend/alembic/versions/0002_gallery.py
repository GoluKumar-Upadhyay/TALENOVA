"""Create gallery categories and gallery image records."""

from alembic import op
import sqlalchemy as sa

revision = "0002_gallery"
down_revision = "0001_initial_auth_and_cms"
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Create gallery tables."""
    op.create_table(
        "gallery_categories",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("uuid", sa.String(36), nullable=False, unique=True),
        sa.Column("name", sa.String(120), nullable=False, unique=True),
        sa.Column("slug", sa.String(140), nullable=False, unique=True),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )
    op.create_table(
        "gallery_images",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("uuid", sa.String(36), nullable=False, unique=True),
        sa.Column("category_id", sa.Integer(), sa.ForeignKey("gallery_categories.id"), nullable=False),
        sa.Column("image_url", sa.String(1000), nullable=False),
        sa.Column("alt_text", sa.String(255), nullable=False),
        sa.Column("caption", sa.Text(), nullable=True),
        sa.Column("display_order", sa.Integer(), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_deleted", sa.Boolean(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    )


def downgrade() -> None:
    """Drop gallery tables."""
    op.drop_table("gallery_images")
    op.drop_table("gallery_categories")
