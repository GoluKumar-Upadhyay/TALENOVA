"""Create footer configuration."""
from alembic import op
import sqlalchemy as sa
revision = "0013_footer"
down_revision = "0012_navigation"
branch_labels = None
depends_on = None
def upgrade() -> None:
    """Create footer singleton storage."""
    op.create_table("footer_configurations", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("uuid", sa.String(36), unique=True), sa.Column("logo_url", sa.String(1000)), sa.Column("description", sa.Text()), sa.Column("sections", sa.JSON()), sa.Column("quick_links", sa.JSON()), sa.Column("contact_details", sa.JSON()), sa.Column("social_links", sa.JSON()), sa.Column("copyright_text", sa.String(500)), sa.Column("newsletter_enabled", sa.Boolean()), sa.Column("newsletter_label", sa.String(255)), sa.Column("legal_links", sa.JSON()), sa.Column("display_order", sa.Integer()), sa.Column("is_active", sa.Boolean()), sa.Column("updated_at", sa.DateTime()))
def downgrade() -> None:
    """Drop footer configuration."""
    op.drop_table("footer_configurations")
