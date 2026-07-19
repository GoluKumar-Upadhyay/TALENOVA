"""Create student success stories table."""
from alembic import op
import sqlalchemy as sa
revision = "0006_success_stories"
down_revision = "0005_testimonials"
branch_labels = None
depends_on = None
def upgrade() -> None:
    """Create success story persistence."""
    op.create_table("success_stories", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("uuid", sa.String(36), unique=True), sa.Column("name", sa.String(180)), sa.Column("image_url", sa.String(1000)), sa.Column("company_logo_url", sa.String(1000)), sa.Column("course", sa.String(255)), sa.Column("batch", sa.String(100)), sa.Column("internship", sa.String(255)), sa.Column("placement", sa.String(255)), sa.Column("job_role", sa.String(180)), sa.Column("college", sa.String(255)), sa.Column("graduation_year", sa.Integer()), sa.Column("salary", sa.String(100)), sa.Column("story", sa.Text()), sa.Column("before_journey", sa.Text()), sa.Column("after_journey", sa.Text()), sa.Column("linkedin_url", sa.String(1000)), sa.Column("achievement_tags", sa.JSON()), sa.Column("is_featured", sa.Boolean()), sa.Column("display_order", sa.Integer()), sa.Column("is_active", sa.Boolean()), sa.Column("is_deleted", sa.Boolean()), sa.Column("created_at", sa.DateTime()), sa.Column("updated_at", sa.DateTime()))
def downgrade() -> None:
    """Drop success stories."""
    op.drop_table("success_stories")
