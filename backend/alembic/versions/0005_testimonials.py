"""Create testimonials table."""
from alembic import op
import sqlalchemy as sa
revision = "0005_testimonials"
down_revision = "0004_achievements"
branch_labels = None
depends_on = None
def upgrade() -> None:
    """Create testimonials."""
    op.create_table("testimonials", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("uuid", sa.String(36), unique=True), sa.Column("student_name", sa.String(180)), sa.Column("college", sa.String(255)), sa.Column("designation", sa.String(180)), sa.Column("course_completed", sa.String(255)), sa.Column("review", sa.Text()), sa.Column("rating", sa.Integer()), sa.Column("photo_url", sa.String(1000)), sa.Column("placement_company", sa.String(255)), sa.Column("package", sa.String(100)), sa.Column("is_featured", sa.Boolean()), sa.Column("display_order", sa.Integer()), sa.Column("is_active", sa.Boolean()), sa.Column("is_deleted", sa.Boolean()), sa.Column("created_at", sa.DateTime()), sa.Column("updated_at", sa.DateTime()))
def downgrade() -> None:
    """Drop testimonials."""
    op.drop_table("testimonials")
