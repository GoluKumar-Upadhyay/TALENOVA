"""Create workshop and training events."""
from alembic import op
import sqlalchemy as sa
revision = "0008_events"
down_revision = "0007_internships"
branch_labels = None
depends_on = None
def upgrade() -> None:
    """Create events table."""
    op.create_table("workshop_events", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("uuid", sa.String(36), unique=True), sa.Column("title", sa.String(255)), sa.Column("description", sa.Text()), sa.Column("event_type", sa.String(80)), sa.Column("start_date", sa.String(40)), sa.Column("end_date", sa.String(40)), sa.Column("registration_deadline", sa.String(40)), sa.Column("location", sa.String(255)), sa.Column("google_maps_url", sa.String(1000)), sa.Column("mode", sa.String(20)), sa.Column("registration_url", sa.String(1000)), sa.Column("banner_url", sa.String(1000)), sa.Column("gallery_urls", sa.JSON()), sa.Column("speaker_details", sa.JSON()), sa.Column("maximum_participants", sa.Integer()), sa.Column("is_featured", sa.Boolean()), sa.Column("display_order", sa.Integer()), sa.Column("is_active", sa.Boolean()), sa.Column("is_deleted", sa.Boolean()), sa.Column("created_at", sa.DateTime()), sa.Column("updated_at", sa.DateTime()))
def downgrade() -> None:
    """Drop events."""
    op.drop_table("workshop_events")
