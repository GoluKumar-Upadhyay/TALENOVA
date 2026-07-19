"""Create the core platform tables omitted by the initial migration chain."""

from alembic import op

from app.db.base import Base
from app.models import cms, content, course, course_category, hero, partner, teacher, video

revision = "0016_missing_core_tables"
down_revision = "0017_milestone_1_auth_rbac"
branch_labels = None
depends_on = None

TABLES = [
    teacher.Teacher.__table__,
    partner.Partner.__table__,
    course_category.CourseCategory.__table__,
    course.Course.__table__,
    course.CourseCurriculumItem.__table__,
    cms.CmsItem.__table__,
    content.ManagedContent.__table__,
    hero.HeroSection.__table__,
    hero.Statistic.__table__,
    video.Video.__table__,
]


def upgrade() -> None:
    """Create each missing table with SQLAlchemy's check-first semantics."""
    Base.metadata.create_all(bind=op.get_bind(), tables=TABLES, checkfirst=True)


def downgrade() -> None:
    """Remove only the tables owned by this migration."""
    for table in reversed(TABLES):
        table.drop(op.get_bind(), checkfirst=True)
