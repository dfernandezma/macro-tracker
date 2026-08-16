import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

import csv
from src.db import connect_db
from src.logger import logger

def importar_alimentos_desde_csv(ruta_archivo: str) -> None:
    # Usamos nuestro escudo protector general
    try:
        with connect_db() as connection:
            with connection.cursor() as cursor:
                # Abrimos el archivo CSV
                with open(ruta_archivo, mode='r', encoding='utf-8') as archivo:
                    # DictReader lee la primera fila como nombres de columnas
                    lector_csv = csv.DictReader(archivo)
                    
                    # Preparamos la consulta SQL
                    query = """
                        INSERT INTO alimentos (nombre, proteinas, carbos, grasas, kcal)
                        VALUES (%s, %s, %s, %s, %s)
                        ON CONFLICT DO NOTHING; -- Evita errores si corres el script 2 veces
                    """
                    
                    contador = 0
                    for fila in lector_csv:
                        # Extraemos los datos basándonos en el nombre de la columna
                        cursor.execute(query, (
                            fila['nombre'],
                            float(fila['proteinas']),
                            float(fila['carbos']),
                            float(fila['grasas']),
                            float(fila['kcal'])
                        ))
                        contador += 1
                
                # Guardamos los cambios
                connection.commit()
                logger.info(f"¡Éxito! Se han importado {contador} alimentos a la base de datos.")
                print(f"¡Éxito! Se han importado {contador} alimentos.")

    except FileNotFoundError:
        logger.error(f"No se encontró el archivo CSV en la ruta: {ruta_archivo}")
        print("Error: No se encontró el archivo CSV.")
    except Exception as e:
        logger.error(f"Fallo al importar alimentos del CSV: {e}")
        print("Hubo un fallo técnico. Revisa el archivo app.log para más detalles.")

# Si ejecutamos este script directamente, lanza la función
if __name__ == "__main__":
    # Asegúrate de que la ruta coincida con donde guardaste el archivo
    importar_alimentos_desde_csv("sql/alimentos_base.csv")