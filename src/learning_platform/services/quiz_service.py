class QuizService:
    def __init__(self, quiz_repository):
        self.quiz_repository = quiz_repository

    def create_quiz(self, course_id, title, questions):
        if not title.strip():
            raise ValueError("Quiz title cannot be empty.")
        if not isinstance(questions, list):
            raise ValueError("Questions must be provided as a list.")
        return self.quiz_repository.create_quiz(course_id, title, questions)
