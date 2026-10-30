from learning_platform.db.mongo_client import create_mongo_database
from learning_platform.db.postgres import PostgresDatabase
from learning_platform.db.redis_client import create_redis_client
from learning_platform.repositories.course_repository import CourseRepository
from learning_platform.repositories.discussion_repository import DiscussionRepository
from learning_platform.repositories.enrollment_repository import EnrollmentRepository
from learning_platform.repositories.progress_repository import ProgressRepository
from learning_platform.repositories.quiz_repository import QuizRepository
from learning_platform.services.dashboard_service import DashboardService
from learning_platform.services.discussion_service import DiscussionService
from learning_platform.services.enrollment_service import EnrollmentService
from learning_platform.services.progress_service import ProgressService
from learning_platform.services.quiz_service import QuizService


def main():
    postgres = PostgresDatabase()
    redis_client = create_redis_client()
    mongo_client, mongo_database = create_mongo_database()

    # Dependency injection: construct dependencies here and pass them in.
    course_repo = CourseRepository(postgres)
    enrollment_repo = EnrollmentRepository(postgres)
    progress_repo = ProgressRepository(postgres)
    quiz_repo = QuizRepository(postgres)
    discussion_repo = DiscussionRepository(mongo_database)

    enrollment_service = EnrollmentService(enrollment_repo)
    progress_service = ProgressService(
        progress_repo, course_repo, enrollment_repo, redis_client
    )
    dashboard_service = DashboardService(
        course_repo, enrollment_repo, progress_repo, progress_service
    )
    quiz_service = QuizService(quiz_repo)
    discussion_service = DiscussionService(discussion_repo)

    try:
        courses = course_repo.get_all()
        print("\nCourses:")
        for course in courses:
            print(f"{course[0]} - {course[1]}")

        # Find sample records by stable names rather than assuming their IDs.
        with postgres.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id FROM students WHERE email = %s", ("alex@example.com",)
                )
                student_id = cursor.fetchone()[0]
                cursor.execute(
                    "SELECT id FROM courses WHERE title = %s", ("Python Basics",)
                )
                course_id = cursor.fetchone()[0]
                cursor.execute(
                    """
                    SELECT l.id
                    FROM lessons l
                    JOIN modules m ON m.id = l.module_id
                    WHERE m.course_id = %s
                    ORDER BY l.position
                    LIMIT 1
                    """,
                    (course_id,),
                )
                lesson_row = cursor.fetchone()

        try:
            enrollment_id = enrollment_service.enroll_student(student_id, course_id)
            print(f"\nEnrollment created: {enrollment_id}")
        except Exception as error:
            # Re-running the demo may encounter the unique enrollment constraint.
            print(f"Enrollment not created: {error}")

        if lesson_row and enrollment_repo.is_enrolled(student_id, course_id):
            progress_service.complete_lesson(student_id, lesson_row[0])
            print("Lesson completion recorded.")

            dashboard = dashboard_service.get_course_progress(student_id, course_id)
            print("Dashboard:", dashboard)

        # MongoDB example:
        thread_id = discussion_service.create_thread(
            course_id, student_id, "What is the difference between a list and tuple?"
        )
        discussion_service.reply(thread_id, student_id, "A tuple is immutable.")

        # JSONB example:
        quiz_id = quiz_service.create_quiz(
            course_id,
            "Practice",
            [{"question": "What is Python?", "answer": "A programming language"}],
        )
        print("Quiz created:", quiz_id)

    finally:
        redis_client.close()
        mongo_client.close()
        postgres.close()


if __name__ == "__main__":
    main()
