class DiscussionService:
    def __init__(self, discussion_repository):
        self.discussion_repository = discussion_repository

    def create_thread(self, course_id, student_id, message):
        if not message.strip():
            raise ValueError("Discussion message cannot be empty.")
        return self.discussion_repository.create_thread(course_id, student_id, message)

    def reply(self, thread_id, student_id, message):
        if not message.strip():
            raise ValueError("Reply cannot be empty.")
        return self.discussion_repository.add_reply(thread_id, student_id, message)

    def get_threads(self, course_id):
        return self.discussion_repository.get_course_threads(course_id)
