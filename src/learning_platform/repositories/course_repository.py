class CourseRepository:
    def __init__(self, database):
        self.database = database

    def get_all(self):
        with self.database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id, title, description FROM courses ORDER BY id")
                return cursor.fetchall()

    def get_lesson_count(self, course_id):
        with self.database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT COUNT(l.id)
                    FROM modules m
                    JOIN lessons l ON l.module_id = m.id
                    WHERE m.course_id = %s
                    """,
                    (course_id,),
                )
                return cursor.fetchone()[0]

    def get_course_id_for_lesson(self, lesson_id):
        with self.database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT m.course_id
                    FROM lessons l
                    JOIN modules m ON m.id = l.module_id
                    WHERE l.id = %s
                    """,
                    (lesson_id,),
                )
                row = cursor.fetchone()
                return row[0] if row else None
