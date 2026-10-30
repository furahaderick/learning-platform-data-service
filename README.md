# Online Learning Platform Data Service

A small Python project covering relational database design,
transactional enrollment, progress tracking, Redis caching, MongoDB discussions,
PostgreSQL JSONB, window functions, and query analysis.

## Setup

```bash
poetry install
cp .env.example .env
docker compose up -d
poetry run python -m learning_platform.setup_database
poetry run python -m learning_platform.seed
poetry run python -m learning_platform.main
```

Run commands from the project root.

## Folder structure

```text
online_learning_platform/
├── docker-compose.yml
├── pyproject.toml
├── .env.example
├── README.md
├── sql/
│   ├── schema.sql
│   └── analytics.sql
└── src/learning_platform/
    ├── config.py
    ├── setup_database.py
    ├── seed.py
    ├── main.py
    ├── db/
    │   ├── postgres.py
    │   ├── redis_client.py
    │   └── mongo_client.py
    ├── repositories/
    │   ├── course_repository.py
    │   ├── enrollment_repository.py
    │   ├── progress_repository.py
    │   ├── quiz_repository.py
    │   └── discussion_repository.py
    └── services/
        ├── enrollment_service.py
        ├── progress_service.py
        ├── dashboard_service.py
        ├── quiz_service.py
        └── discussion_service.py
```

- `db/` creates database connections. PostgreSQL uses `ThreadedConnectionPool`.
- `repositories/` contains SQL and MongoDB persistence operations.
- `services/` contains validation and application rules.
- `sql/` contains the schema and assessment queries.
- `main.py` wires dependencies together and runs a small demonstration.

## Design notes

**Enrollment:** prerequisite verification and enrollment insertion happen inside
one PostgreSQL transaction. If validation or insertion fails, the transaction
rolls back. A unique constraint prevents duplicate enrollments.

**Progress:** a row in `lesson_progress` represents one completed lesson.
Completion is calculated from completed lessons divided by all lessons in a course.
The unique `(student_id, lesson_id)` constraint prevents duplicate completion rows.

**Redis:** the key format is
`student:{student_id}:course:{course_id}:completion`. Values expire after five
minutes. Completing a new lesson invalidates the old value.

**MongoDB:** each discussion thread is a document with a `replies` array.

**JSONB:** quiz questions are stored as a JSON array in PostgreSQL.

## Analytics

Run `sql/analytics.sql` in a PostgreSQL client. It includes:

1. Completion percentage per enrolled course using grouped subqueries.
2. `LAG()` to compare lesson completion times.
3. `EXPLAIN ANALYZE` for a student dashboard query.
