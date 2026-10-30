class ProgressService:
    def __init__(
        self,
        progress_repository,
        course_repository,
        enrollment_repository,
        redis_client,
    ):
        self.progress_repository = progress_repository
        self.course_repository = course_repository
        self.enrollment_repository = enrollment_repository
        self.redis_client = redis_client

    def complete_lesson(self, student_id, lesson_id):
        course_id = self.course_repository.get_course_id_for_lesson(lesson_id)
        if course_id is None:
            raise ValueError("Lesson does not exist.")

        if not self.enrollment_repository.is_enrolled(student_id, course_id):
            raise ValueError("Student must be enrolled in this course.")

        inserted = self.progress_repository.mark_lesson_completed(student_id, lesson_id)
        if inserted:
            key = f"student:{student_id}:course:{course_id}:completion"
            self.redis_client.delete(key)
        return inserted

    def get_completion_percentage(self, student_id, course_id):
        key = f"student:{student_id}:course:{course_id}:completion"
        cached = self.redis_client.get(key)
        if cached is not None:
            return float(cached)

        percentage = self.progress_repository.get_completion_percentage(
            student_id, course_id
        )
        self.redis_client.setex(key, 300, str(percentage))
        return percentage
