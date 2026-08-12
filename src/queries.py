import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.db import connect_db
from src.calculator import calculate
from src.logger import logger

import datetime

def get_info(
        user_id: int
    ) -> list[float, float, float, float]:

    with connect_db() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute("""
                    SELECT sexo, edad, altura_cm, peso_kg, nivel_actividad, objetivo
                    FROM usuarios
                    WHERE id = %s;
                """, (user_id,))

                result = cursor.fetchone()

                if result is None:
                    logger.warning(f"Error al obtener detalles del usuario ({user_id}).")
                    return None

                sex, age, height, weight, activity, objective = result

                weight = float(weight)

                return calculate(sex, age, height, weight, activity, objective)

            except Exception as e:
                logger.error(f"Error al consultar Base de Datos: {e}. Peticion usuario {user_id}")
                return None

def get_current(
        user_id: int,
        date: datetime.date
    ) -> tuple[float, float, float] | None:

    with connect_db() as connection:
        with connection.cursor() as cursor:
            try:
                cursor.execute("""
                    SELECT
                        COALESCE(SUM(a.kcal * r.gramos / 100.0), 0) AS total_kcal
                        COALESCE(SUM(a.proteinas * r.gramos / 100.0), 0) AS total_proteinas,
                        COALESCE(SUM(a.grasas * r.gramos / 100.0), 0) AS total_grasas,
                        COALESCE(SUM(a.carbos * r.gramos / 100.0), 0) AS total_carb
                    FROM registros r
                    JOIN alimentos a ON r.id_alimento = a.id
                    WHERE r.id_usuario = %s AND r.fecha::date = %s;
                """, (user_id, date))

                result = cursor.fetchone()

                if result is None:
                    logger.warning(f"No se encontró información en la consulta de macros actuales (usuario {user_id})")
                    return None

                kcal, protein, fat, carb = result

                return [float(kcal), float(protein), float(fat), float(carb)]

            except Exception as e:
                logger.error(f"Error al consultar base de datos {e}. Petición del usuario {user_id}")
                return None