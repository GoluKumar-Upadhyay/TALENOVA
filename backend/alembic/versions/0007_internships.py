"""Create internship programme records."""
from alembic import op
import sqlalchemy as sa
revision = "0007_internships"
down_revision = "0006_success_stories"
branch_labels = None
depends_on = None
def upgrade() -> None:
    """Create internships."""
    op.create_table("internship_programs", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("uuid", sa.String(36), unique=True), sa.Column("title", sa.String(255)), sa.Column("description", sa.Text()), sa.Column("company", sa.String(255)), sa.Column("company_logo_url", sa.String(1000)), sa.Column("internship_type", sa.String(20)), sa.Column("duration", sa.String(100)), sa.Column("stipend", sa.String(100)), sa.Column("location", sa.String(255)), sa.Column("eligibility", sa.Text()), sa.Column("application_url", sa.String(1000)), sa.Column("last_date", sa.String(40)), sa.Column("skills", sa.JSON()), sa.Column("is_coming_soon", sa.Boolean()), sa.Column("is_featured", sa.Boolean()), sa.Column("display_order", sa.Integer()), sa.Column("is_active", sa.Boolean()), sa.Column("is_deleted", sa.Boolean()), sa.Column("created_at", sa.DateTime()), sa.Column("updated_at", sa.DateTime()))
def downgrade() -> None:
    """Drop internships."""
    op.drop_table("internship_programs")
