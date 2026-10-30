class EnrollmentService:
    def __init__(self, enrollment_repository):
        self.enrollment_repository = enrollment_repository

    def enroll_student(self, student_id, course_id):
        if student_id <= 0 or course_id <= 0:
            raise ValueError("Student ID and course ID must be positive.")
        return self.enrollment_repository.enroll(student_id, course_id)
