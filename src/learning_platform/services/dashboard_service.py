class DashboardService:
    def __init__(
        self,
        course_repository,
        enrollment_repository,
        progress_repository,
        progress_service,
    ):
        self.course_repository = course_repository
        self.enrollment_repository = enrollment_repository
        self.progress_repository = progress_repository
        self.progress_service = progress_service

    def get_course_progress(self, student_id, course_id):
        if not self.enrollment_repository.is_enrolled(student_id, course_id):
            raise ValueError("Student is not enrolled in this course.")

        completed = self.progress_repository.get_completed_count(student_id, course_id)
        total = self.course_repository.get_lesson_count(course_id)
        percentage = self.progress_service.get_completion_percentage(
            student_id, course_id
        )
        return {
            "student_id": student_id,
            "course_id": course_id,
            "completed_lessons": completed,
            "total_lessons": total,
            "completion_percentage": percentage,
        }
