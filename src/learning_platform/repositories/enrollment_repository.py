class EnrollmentRepository:
    def __init__(self, database):
        self.database = database

    def enroll(self, student_id, course_id):
        # The prerequisite check and insert are part of the same transaction.
        with self.database.connection() as connection:
            try:
                with connection.cursor() as cursor:
                    cursor.execute(
                        """
                        SELECT prerequisite_course_id
                        FROM course_prerequisites
                        WHERE course_id = %s
                        """,
                        (course_id,),
                    )
                    prerequisite_ids = [row[0] for row in cursor.fetchall()]

                    if prerequisite_ids:
                        cursor.execute(
                            """
                            SELECT COUNT(*)
                            FROM course_prerequisites cp
                            WHERE cp.course_id = %s
                                AND EXISTS (
                                    SELECT 1
                                    FROM enrollments e
                                    WHERE e.student_id = %s
                                        AND e.course_id = cp.prerequisite_course_id
                                )
                                AND NOT EXISTS (
                                    SELECT 1
                                    FROM modules m
                                    JOIN lessons l ON l.module_id = m.id
                                    WHERE m.course_id = cp.prerequisite_course_id
                                    AND NOT EXISTS (
                                        SELECT 1 FROM lesson_progress lp
                                        WHERE lp.student_id = %s
                                            AND lp.lesson_id = l.id
                                    )
                                )
                            """,
                            (course_id, student_id, student_id),
                        )
                        completed_count = cursor.fetchone()[0]
                        if completed_count != len(prerequisite_ids):
                            raise ValueError(
                                "Complete all prerequisite courses before enrolling."
                            )

                    cursor.execute(
                        """
                        INSERT INTO enrollments (student_id, course_id)
                        VALUES (%s, %s)
                        RETURNING id
                        """,
                        (student_id, course_id),
                    )
                    enrollment_id = cursor.fetchone()[0]

                connection.commit()
                return enrollment_id
            except Exception:
                connection.rollback()
                raise

    def is_enrolled(self, student_id, course_id):
        with self.database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT EXISTS (
                        SELECT 1 FROM enrollments
                        WHERE student_id = %s AND course_id = %s
                    )
                    """,
                    (student_id, course_id),
                )
                return cursor.fetchone()[0]
