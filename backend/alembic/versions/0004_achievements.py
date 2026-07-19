"""Create achievements table."""
from alembic import op
import sqlalchemy as sa
revision = "0004_achievements"
down_revision = "0003_projects"
branch_labels = None
depends_on = None
def upgrade() -> None:
    """Create achievement storage."""
    op.create_table("achievements", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("uuid", sa.String(36), unique=True), sa.Column("title", sa.String(255)), sa.Column("description", sa.Text()), sa.Column("image_url", sa.String(1000)), sa.Column("achievement_type", sa.String(100)), sa.Column("is_featured", sa.Boolean()), sa.Column("display_order", sa.Integer()), sa.Column("is_active", sa.Boolean()), sa.Column("is_deleted", sa.Boolean()), sa.Column("created_at", sa.DateTime()), sa.Column("updated_at", sa.DateTime()))
def downgrade() -> None:
    """Drop achievements."""
    op.drop_table("achievements")
