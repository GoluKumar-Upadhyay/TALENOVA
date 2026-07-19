"""Create project portfolio table."""
from alembic import op
import sqlalchemy as sa
revision = "0003_projects"
down_revision = "0002_gallery"
branch_labels = None
depends_on = None
def upgrade() -> None:
    """Create projects."""
    op.create_table("projects", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("uuid", sa.String(36), unique=True), sa.Column("title", sa.String(255)), sa.Column("description", sa.Text()), sa.Column("image_url", sa.String(1000)), sa.Column("github_url", sa.String(1000)), sa.Column("demo_url", sa.String(1000)), sa.Column("technologies", sa.JSON()), sa.Column("tags", sa.JSON()), sa.Column("screenshot_urls", sa.JSON()), sa.Column("status", sa.String(20)), sa.Column("is_featured", sa.Boolean()), sa.Column("display_order", sa.Integer()), sa.Column("is_active", sa.Boolean()), sa.Column("is_deleted", sa.Boolean()), sa.Column("created_at", sa.DateTime()), sa.Column("updated_at", sa.DateTime()))
def downgrade() -> None:
    """Drop projects."""
    op.drop_table("projects")
