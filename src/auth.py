import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.db import connect_db
from src.logger import logger

import bcrypt
import streamlit as st


def register_user(
    email: str,
    passwd: str,
    sex: str,
    activity: str,
    objective: str,
    height: int,
    age: int,
    weight: float,
) -> int | None:

    salt = bcrypt.gensalt()
    password_hash = bcrypt.hashpw(passwd.encode("utf-8"), salt)

    try:
        with connect_db() as connection:
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO usuarios (email, password_hash, sexo, nivel_actividad, objetivo, altura_cm, edad, peso_kg)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    RETURNING id;
                """

                cursor.execute(
                    query,
                    (
                        email,
                        password_hash.decode("utf-8"),
                        sex,
                        activity,
                        objective,
                        height,
                        age,
                        weight,
                    ),
                )

                user_id = cursor.fetchone()[0]

                logger.info(f"Nuevo usuario registrado (ID: {user_id}, email: {email})")

                connection.commit()

                return user_id

    except Exception as e:
        logger.error(f"Error al registrar usuario (email: {email}). Detalle {e}")
        return None


def login_user(email: str, passwd: str) -> int | None:

    try:
        with connect_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT id, password_hash FROM usuarios WHERE email = %s;", (email,)
                )

                result = cursor.fetchone()

                # email not fount
                if not result:
                    logger.warning(f"Correo no encontrado ({email})")
                    return None

                user_id, passwd_hash = result

                if bcrypt.checkpw(passwd.encode("utf-8"), passwd_hash.encode("utf-8")):
                    logger.info(
                        f"Nuevo inicio de sesión (ID: {user_id}, email: {email})"
                    )
                    return user_id
                else:
                    logger.warning(
                        f"Contraseña incorrecta (ID: {user_id}, email: {email})"
                    )
                    return None  # incorrect password

    except Exception as e:
        logger.error(f"Error al hacer inicio de sesión (email: {email}). Detalle: {e}")
        return None


def verify_email(email: str) -> bool:

    try:
        with connect_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute("SELECT id FROM usuarios WHERE email = %s;", (email,))

                return cursor.fetchone() is not None

    except Exception as e:
        logger.error(f"Error al verificar email (email: {email}). Detalle: {e}")
        return False


def logout_user():
    st.session_state["user_id"] = None
    st.rerun()
