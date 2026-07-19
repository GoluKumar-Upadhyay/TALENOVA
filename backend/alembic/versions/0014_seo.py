"""Create SEO metadata records."""
from alembic import op
import sqlalchemy as sa
revision = "0014_seo"
down_revision = "0013_footer"
branch_labels = None
depends_on = None
def upgrade() -> None:
    """Create SEO configuration."""
    op.create_table("seo_records", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("uuid", sa.String(36), unique=True), sa.Column("page_key", sa.String(120), unique=True), sa.Column("site_title", sa.String(255)), sa.Column("meta_title", sa.String(255)), sa.Column("meta_description", sa.Text()), sa.Column("meta_keywords", sa.JSON()), sa.Column("canonical_url", sa.String(1000)), sa.Column("robots_meta", sa.String(120)), sa.Column("open_graph", sa.JSON()), sa.Column("twitter_cards", sa.JSON()), sa.Column("structured_data", sa.JSON()), sa.Column("sitemap_config", sa.JSON()), sa.Column("robots_txt", sa.Text()), sa.Column("verification_codes", sa.JSON()), sa.Column("redirect_rules", sa.JSON()), sa.Column("hreflang", sa.JSON()), sa.Column("favicon_url", sa.String(1000)), sa.Column("is_active", sa.Boolean()), sa.Column("updated_at", sa.DateTime()))
def downgrade() -> None:
    """Drop SEO records."""
    op.drop_table("seo_records")
