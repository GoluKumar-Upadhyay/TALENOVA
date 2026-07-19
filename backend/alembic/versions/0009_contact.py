"""Create contact messages table."""
from alembic import op
import sqlalchemy as sa
revision = "0009_contact"
down_revision = "0008_events"
branch_labels = None
depends_on = None
def upgrade() -> None:
    """Create contact message storage."""
    op.create_table("contact_messages", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("uuid", sa.String(36), unique=True), sa.Column("contact_type", sa.String(20)), sa.Column("name", sa.String(180)), sa.Column("email", sa.String(255)), sa.Column("phone", sa.String(40)), sa.Column("organization", sa.String(255)), sa.Column("designation", sa.String(180)), sa.Column("website", sa.String(1000)), sa.Column("course_interested", sa.String(255)), sa.Column("training_requirements", sa.Text()), sa.Column("expected_students", sa.Integer()), sa.Column("preferred_dates", sa.String(255)), sa.Column("subject", sa.String(255)), sa.Column("message", sa.Text()), sa.Column("status", sa.String(30)), sa.Column("is_read", sa.Boolean()), sa.Column("is_archived", sa.Boolean()), sa.Column("created_at", sa.DateTime()), sa.Column("updated_at", sa.DateTime()))
def downgrade() -> None:
    """Drop contact messages."""
    op.drop_table("contact_messages")
