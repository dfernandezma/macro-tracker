import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.logger import logger

import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()


def connect_db(
    host: str = os.getenv("DB_HOST", ""),
    database: str = os.getenv("DB_NAME", ""),
    user: str = os.getenv("DB_USER", ""),
    password: str = os.getenv("DB_PASSWORD", ""),
    port: int = os.getenv("DB_PORT", ""),
) -> psycopg2.extensions.connection:

    try:
        connection = psycopg2.connect(
            host=host, database=database, user=user, password=password, port=port
        )
        return connection

    except Exception as error:
        logger.error(f"Error al conectar a la Base de Datos. Detalle: {error}")
        raise
