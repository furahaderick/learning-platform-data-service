class ProgressRepository:
    def __init__(self, database):
        self.database = database

    def mark_lesson_completed(self, student_id, lesson_id):
        with self.database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO lesson_progress (student_id, lesson_id)
                    VALUES (%s, %s)
                    ON CONFLICT (student_id, lesson_id) DO NOTHING
                    RETURNING id
                    """,
                    (student_id, lesson_id),
                )
                inserted = cursor.fetchone() is not None
            connection.commit()
            return inserted

    def get_completed_count(self, student_id, course_id):
        with self.database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT COUNT(*)
                    FROM lesson_progress lp
                    JOIN lessons l ON l.id = lp.lesson_id
                    JOIN modules m ON m.id = l.module_id
                    WHERE lp.student_id = %s AND m.course_id = %s
                    """,
                    (student_id, course_id),
                )
                return cursor.fetchone()[0]

    def get_completion_percentage(self, student_id, course_id):
        with self.database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        (SELECT COUNT(*)
                         FROM lesson_progress lp
                         JOIN lessons l ON l.id = lp.lesson_id
                         JOIN modules m ON m.id = l.module_id
                         WHERE lp.student_id = %s AND m.course_id = %s),
                        (SELECT COUNT(*)
                         FROM lessons l
                         JOIN modules m ON m.id = l.module_id
                         WHERE m.course_id = %s)
                    """,
                    (student_id, course_id, course_id),
                )
                completed, total = cursor.fetchone()

        if total == 0:
            return 0.0
        return round(completed * 100.0 / total, 2)
