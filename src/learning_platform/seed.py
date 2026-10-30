from psycopg2.extras import Json

from learning_platform.db.postgres import PostgresDatabase


def main():
    database = PostgresDatabase()
    try:
        with database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO students (name, email)
                    VALUES ('Alex Student', 'alex@example.com')
                    ON CONFLICT (email) DO UPDATE SET name = EXCLUDED.name
                    RETURNING id
                    """
                )
                student_id = cursor.fetchone()[0]

                cursor.execute(
                    """
                    INSERT INTO courses (title, description)
                    VALUES ('Python Basics', 'An introduction to Python.')
                    ON CONFLICT (title) DO UPDATE
                    SET description = EXCLUDED.description
                    RETURNING id
                    """
                )
                basics_id = cursor.fetchone()[0]

                cursor.execute(
                    """
                    INSERT INTO courses (title, description)
                    VALUES ('Python Advanced', 'More advanced Python topics.')
                    ON CONFLICT (title) DO UPDATE
                    SET description = EXCLUDED.description
                    RETURNING id
                    """
                )
                advanced_id = cursor.fetchone()[0]

                cursor.execute(
                    """
                    INSERT INTO course_prerequisites
                        (course_id, prerequisite_course_id)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                    """,
                    (advanced_id, basics_id),
                )

                cursor.execute(
                    """
                    INSERT INTO modules (course_id, title, position)
                    VALUES (%s, 'Getting Started', 1)
                    ON CONFLICT (course_id, position) DO UPDATE
                    SET title = EXCLUDED.title
                    RETURNING id
                    """,
                    (basics_id,),
                )
                module_id = cursor.fetchone()[0]

                cursor.execute(
                    """
                    INSERT INTO lessons (module_id, title, position)
                    VALUES (%s, 'Installing Python', 1),
                            (%s, 'Variables and Types', 2)
                    ON CONFLICT (module_id, position) DO UPDATE
                    SET title = EXCLUDED.title
                    RETURNING id
                    """,
                    (module_id, module_id),
                )
                lesson_ids = [row[0] for row in cursor.fetchall()]

                cursor.execute(
                    """
                    INSERT INTO quizzes (course_id, title, questions)
                    SELECT %s, 'Python Basics Quiz', %s
                    WHERE NOT EXISTS (
                        SELECT 1 FROM quizzes
                        WHERE course_id = %s AND title = 'Python Basics Quiz'
                    )
                    """,
                    (
                        basics_id,
                        Json(
                            [
                                {
                                    "question": "Which keyword defines a function?",
                                    "options": ["func", "def", "function"],
                                    "answer": "def",
                                }
                            ]
                        ),
                        basics_id,
                    ),
                )
            connection.commit()

        print("Sample data is ready.")
        print(f"Student ID: {student_id}")
        print(f"Python Basics course ID: {basics_id}")
        print(f"Python Advanced course ID: {advanced_id}")
        print(f"Lesson IDs: {lesson_ids}")
    finally:
        database.close()


if __name__ == "__main__":
    main()
