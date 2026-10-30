from contextlib import contextmanager
from psycopg2.pool import ThreadedConnectionPool
from learning_platform.config import postgres_settings


class PostgresDatabase:
    def __init__(self):
        self.pool = ThreadedConnectionPool(minconn=1, maxconn=10, **postgres_settings())

    @contextmanager
    def connection(self):
        connection = self.pool.getconn()
        try:
            yield connection
        finally:
            # Clear any unfinished read transaction before reusing the connection.
            connection.rollback()
            self.pool.putconn(connection)

    def close(self):
        self.pool.closeall()
