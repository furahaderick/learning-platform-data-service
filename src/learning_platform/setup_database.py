from pathlib import Path
from learning_platform.db.postgres import PostgresDatabase


def main():
    database = PostgresDatabase()
    schema_file = Path(__file__).resolve().parents[2] / "sql" / "schema.sql"
    try:
        with database.connection() as connection:
            with connection.cursor() as cursor:
                cursor.execute(schema_file.read_text(encoding="utf-8"))
            connection.commit()
        print("Database schema created.")
    finally:
        database.close()


if __name__ == "__main__":
    main()
