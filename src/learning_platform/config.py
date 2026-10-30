import os
from dotenv import load_dotenv

load_dotenv()


def postgres_settings():
    return {
        "host": os.getenv("POSTGRES_HOST", "localhost"),
        "port": int(os.getenv("POSTGRES_PORT", "5432")),
        "dbname": os.getenv("POSTGRES_DB", "learning_platform"),
        "user": os.getenv("POSTGRES_USER", "postgres"),
        "password": os.getenv("POSTGRES_PASSWORD", "postgres"),
    }


def redis_url():
    host = os.getenv("REDIS_HOST", "localhost")
    port = os.getenv("REDIS_PORT", "6379")
    db = os.getenv("REDIS_DB", "0")
    return f"redis://{host}:{port}/{db}"


def mongo_settings():
    return {
        "uri": os.getenv("MONGO_URI", "mongodb://localhost:27017/"),
        "database": os.getenv("MONGO_DB", "learning_platform"),
    }
