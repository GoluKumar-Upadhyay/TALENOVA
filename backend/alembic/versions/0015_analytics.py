"""Create analytics events."""
from alembic import op
import sqlalchemy as sa
revision = "0015_analytics"
down_revision = "0014_seo"
branch_labels = None
depends_on = None
def upgrade() -> None:
    """Create indexed analytics events."""
    op.create_table("analytics_events", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("uuid", sa.String(36), unique=True), sa.Column("event_type", sa.String(80)), sa.Column("occurred_at", sa.DateTime()), sa.Column("metadata", sa.JSON()))
    op.create_index("ix_analytics_events_type_time", "analytics_events", ["event_type", "occurred_at"])
def downgrade() -> None:
    """Drop analytics events."""
    op.drop_index("ix_analytics_events_type_time", table_name="analytics_events")
    op.drop_table("analytics_events")
