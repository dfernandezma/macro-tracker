import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.db import connect_db
from src.calculator import calculate
from src.logger import logger

import datetime
import pandas as pd


def get_info(user_id: int) -> list[float, float, float, float]:

    try:
        with connect_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT sexo, edad, altura_cm, peso_kg, nivel_actividad, objetivo
                    FROM usuarios
                    WHERE id = %s;
                """,
                    (user_id,),
                )

                result = cursor.fetchone()

                if result is None:
                    logger.warning(
                        f"Error al obtener detalles del usuario ({user_id})."
                    )
                    return None

                sex, age, height, weight, activity, objective = result

                weight = float(weight)

                return calculate(sex, age, height, weight, activity, objective)

    except Exception as e:
        logger.error(
            f"Error al obtener información nutricional de usuario (ID: {user_id}). Detalle: {e}"
        )
        return None


def get_current(user_id: int, date: datetime.date) -> tuple[float, float, float] | None:

    try:
        with connect_db() as connection:
            with connection.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT
                        COALESCE(SUM(a.kcal * r.gramos / 100.0), 0) AS total_kcal,
                        COALESCE(SUM(a.proteinas * r.gramos / 100.0), 0) AS total_proteinas,
                        COALESCE(SUM(a.grasas * r.gramos / 100.0), 0) AS total_grasas,
                        COALESCE(SUM(a.carbos * r.gramos / 100.0), 0) AS total_carb
                    FROM registros r
                    JOIN alimentos a ON r.id_alimento = a.id
                    WHERE r.id_usuario = %s AND r.fecha::date = %s;
                """,
                    (user_id, date),
                )

                result = cursor.fetchone()
                logger.info(f"Resultado consulta: {result}")

                if result is None:
                    logger.warning(
                        f"No se encontró información en la consulta de macros actuales (usuario {user_id})"
                    )
                    return None

                kcal, protein, fat, carb = result

                return [float(kcal), float(protein), float(fat), float(carb)]

    except Exception as e:
        logger.error(
            f"Error al obtener información diaria del usuario (ID: {user_id}. Detalle: {e})"
        )
        return None


def get_records(user_id: int, date: datetime.date) -> pd.DataFrame | None:

    try:
        with connect_db() as connection:
            with connection.cursor() as cursor:
                query = """
                        SELECT
                            r.fecha,
                            a.nombre,
                            r.gramos,
                            a.kcal * r.gramos / 100.0 AS kcal_consumidas,
                            a.proteinas * r.gramos / 100.0 AS proteinas_consumidas,
                            a.grasas * r.gramos / 100.0 AS grasas_consumidas,
                            a.carbos * r.gramos / 100.0 AS carbos_consumidos
                        FROM alimentos a
                        JOIN registros r ON a.id = r.id_alimento
                        WHERE r.id_usuario = %s AND r.fecha::date = %s;
                    """
                cursor.execute(query, (user_id, date))
                result = cursor.fetchall()

                if result is None:
                    logger.warning(
                        f"No se ha encontrado información de registros diario (ID: {user_id})"
                    )
                    return None

                df = pd.DataFrame(
                    result,
                    columns=[
                        "Fecha",
                        "Alimento",
                        "Cantidad (g)",
                        "Kcal totales",
                        "Proteínas totales (g)",
                        "Grasas totales (g)",
                        "Carbohidratos totales (g)",
                    ],
                )

                return df
    except Exception as e:
        logger.error(
            f"Error en consulta de registros diarios (ID: {user_id}). Detalle: {e}"
        )
        return None


def get_foods() -> dict[str:int] | None:

    try:
        with connect_db() as connection:
            with connection.cursor() as cursor:
                query = """
                    SELECT nombre, id
                    FROM alimentos;
                """
                cursor.execute(query)
                result = cursor.fetchall()

                if result is None:
                    logger.warning("No se encontró alimentos en la base de datos")
                    return None

                return {name: int(id) for name, id in result}

    except Exception as e:
        logger.error(
            f"Error al obtener lista de alimentos de la base de datos. Detalle: {e}"
        )
        return None


def add_food(user_id: int, food_id: int, amount: float, date: datetime) -> int | None:

    try:
        with connect_db() as connection:
            with connection.cursor() as cursor:
                query = """
                    INSERT INTO registros (id_usuario, id_alimento, gramos, fecha)
                    VALUES (%s, %s, %s, %s)
                    RETURNING id;
                """

                cursor.execute(query, (user_id, food_id, amount, date))

                record_id = cursor.fetchone()[0]
                logger.info(f"Inserción de registro (usuario: {user_id})")
                return record_id

    except Exception as e:
        logger.error(
            f"Error insertando registro diario (usuario: {user_id}). Detalle: {e}"
        )
        return None
