"""Create navigation items."""
from alembic import op
import sqlalchemy as sa
revision = "0012_navigation"
down_revision = "0011_settings"
branch_labels = None
depends_on = None
def upgrade() -> None:
    """Create hierarchical navigation storage."""
    op.create_table("navigation_items", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("uuid", sa.String(36), unique=True), sa.Column("parent_id", sa.Integer(), sa.ForeignKey("navigation_items.id")), sa.Column("label", sa.String(120)), sa.Column("icon", sa.String(80)), sa.Column("href", sa.String(1000)), sa.Column("is_external", sa.Boolean()), sa.Column("visible_roles", sa.JSON()), sa.Column("location", sa.String(20)), sa.Column("is_mega_menu", sa.Boolean()), sa.Column("open_in_new_tab", sa.Boolean()), sa.Column("authentication_required", sa.Boolean()), sa.Column("display_order", sa.Integer()), sa.Column("is_active", sa.Boolean()), sa.Column("created_at", sa.DateTime()), sa.Column("updated_at", sa.DateTime()))
def downgrade() -> None:
    """Drop navigation."""
    op.drop_table("navigation_items")
