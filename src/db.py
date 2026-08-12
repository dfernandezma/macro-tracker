import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def connect_db(
        host: str = "localhost",
        database: str = "macro_db",
        user: str = "adminfmmv",
        password: str = os.getenv("DB_PASSWORD", ""),
        port: int = 5432
    ) -> psycopg2.extensions.connection:

    try:
        connection = psycopg2.connect(
            host=host,
            database=database,
            user=user,
            password=password,
            port=port
        )

    except Exception as error:
        print(f"Error al conectar a la Base de Datos. {error}")

    return connection