"""Contact request validation tests."""
from app.schemas.contact import ContactWrite
def test_student_contact_supports_course_interest() -> None:
    """Student contact payload includes the interested course."""
    data = ContactWrite(contact_type="student", name="Student", email="student@example.com", subject="Course", message="I need information about a course", course_interested="AI")
    assert data.course_interested == "AI"
