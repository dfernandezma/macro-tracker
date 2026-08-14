import sys
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

from src.constants import MAP_ACTIVITY_NUM


def calculate_bmr(sex: str, age: int, weight: float, height: float) -> float:
    if sex == "Hombre":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    return bmr


def calculate_kcal(objective: str, bmr: float, activity: str) -> float:
    tdee = bmr * MAP_ACTIVITY_NUM[activity]

    if objective == "Ganar masa muscular":
        return tdee + 500
    elif objective == "Bajar de peso":
        return tdee - 500
    else:
        return tdee


def calculate_protein(objective: str, weight: float) -> float:
    if objective == "Ganar masa muscular":
        return weight * 2
    else:
        return weight * 2.5


def calculate_fat(kcal: float) -> float:
    return 0.3 * kcal / 9


def calculate_carb(kcal: float, protein: float, fat: float) -> float:
    return (kcal - protein * 4 - fat * 9) / 4


def calculate(
    sex: str, age: int, height: int, weight: float, activity: str, objective: str
) -> list[float, float, float, float]:
    bmr = calculate_bmr(sex, age, weight, height)
    kcal = calculate_kcal(objective, bmr, activity)
    protein = calculate_protein(objective, weight)
    fat = calculate_fat(kcal)
    carb = calculate_carb(kcal, protein, fat)

    return [bmr, kcal, protein, fat, carb]
