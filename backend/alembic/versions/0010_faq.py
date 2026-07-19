"""Create frequently asked questions."""
from alembic import op
import sqlalchemy as sa
revision = "0010_faq"
down_revision = "0009_contact"
branch_labels = None
depends_on = None
def upgrade() -> None:
    """Create FAQ records."""
    op.create_table("faqs", sa.Column("id", sa.Integer(), primary_key=True), sa.Column("uuid", sa.String(36), unique=True), sa.Column("question", sa.String(500)), sa.Column("answer", sa.Text()), sa.Column("page", sa.String(80)), sa.Column("category", sa.String(40)), sa.Column("seo_slug", sa.String(180), unique=True), sa.Column("is_featured", sa.Boolean()), sa.Column("view_count", sa.Integer()), sa.Column("helpful_count", sa.Integer()), sa.Column("not_helpful_count", sa.Integer()), sa.Column("display_order", sa.Integer()), sa.Column("is_active", sa.Boolean()), sa.Column("is_deleted", sa.Boolean()), sa.Column("created_at", sa.DateTime()), sa.Column("updated_at", sa.DateTime()))
def downgrade() -> None:
    """Drop FAQs."""
    op.drop_table("faqs")
