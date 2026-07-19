"""Create website settings singleton."""
from alembic import op
import sqlalchemy as sa
revision = "0011_settings"
down_revision = "0010_faq"
branch_labels = None
depends_on = None
def upgrade() -> None:
    """Create website settings."""
    op.create_table("website_settings", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("uuid", sa.String(36), unique=True), sa.Column("site_name", sa.String(255)), sa.Column("tagline", sa.String(255)), sa.Column("default_language", sa.String(20)), sa.Column("timezone", sa.String(80)), sa.Column("site_logo_url", sa.String(1000)), sa.Column("favicon_url", sa.String(1000)), sa.Column("hero_defaults", sa.JSON()), sa.Column("contact_information", sa.JSON()), sa.Column("social_links", sa.JSON()), sa.Column("email_settings", sa.JSON()), sa.Column("theme_settings", sa.JSON()), sa.Column("homepage_configuration", sa.JSON()), sa.Column("analytics_keys", sa.JSON()), sa.Column("seo_defaults", sa.JSON()), sa.Column("maintenance_mode", sa.Boolean()), sa.Column("maintenance_message", sa.String(1000)), sa.Column("default_theme", sa.String(30)), sa.Column("pagination_size", sa.Integer()), sa.Column("updated_at", sa.DateTime()))
def downgrade() -> None:
    """Drop website settings."""
    op.drop_table("website_settings")
