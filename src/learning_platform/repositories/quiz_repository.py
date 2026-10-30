from psycopg2.extras import Json


class QuizRepository:
    def __init__(self, database):
        self.database = database

    def create_quiz(self, course_id, title, questions):
        with self.database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO quizzes (course_id, title, questions)
                    VALUES (%s, %s, %s)
                    RETURNING id
                    """,
                    (course_id, title, Json(questions)),
                )
                quiz_id = cursor.fetchone()[0]
            connection.commit()
            return quiz_id

    def get_quiz(self, quiz_id):
        with self.database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, course_id, title, questions FROM quizzes WHERE id = %s",
                    (quiz_id,),
                )
                return cursor.fetchone()
