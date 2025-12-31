from __future__ import annotations

import random
from dataclasses import dataclass
from typing import Literal, Dict, List

from foods import FOODS

Gender = Literal["male", "female"]
Goal = Literal["lose", "maintain", "gain"]
Activity = Literal["low", "medium", "high"]
MealsPerDay = Literal[3, 4, 5]


@dataclass
class UserProfile:
    age: int
    gender: Gender
    height_cm: float
    weight_kg: float
    activity: Activity
    goal: Goal
    meals_per_day: MealsPerDay


def calc_bmr(profile: UserProfile) -> float:
    # Mifflin-St Jeor
    if profile.gender == "male":
        return 10 * profile.weight_kg + 6.25 * profile.height_cm - 5 * profile.age + 5
    return 10 * profile.weight_kg + 6.25 * profile.height_cm - 5 * profile.age - 161


def activity_factor(activity: Activity) -> float:
    return {"low": 1.2, "medium": 1.55, "high": 1.725}[activity]


def target_calories(profile: UserProfile) -> int:
    tdee = calc_bmr(profile) * activity_factor(profile.activity)

    if profile.goal == "lose":
        tdee -= 400
    elif profile.goal == "gain":
        tdee += 300

    tdee = max(tdee, 1200)
    return int(round(tdee))


def _pick_item(items: List[dict], used: set[str]) -> dict:

    candidates = [x for x in items if x["name"] not in used]
    if not candidates:
        candidates = items
    return random.choice(candidates)


def generate_day_plan(profile: UserProfile, kcal_target: int, used: set[str]) -> Dict:
    meals = []
    total = 0

    if profile.meals_per_day == 3:
        types = ["breakfast", "lunch", "dinner"]
    elif profile.meals_per_day == 4:
        types = ["breakfast", "lunch", "dinner", "snack"]
    else:
        types = ["breakfast", "lunch", "dinner", "snack", "snack"]

    for meal_type in types:
        item = _pick_item(FOODS[meal_type], used)
        used.add(item["name"])
        meals.append({"type": meal_type, "name": item["name"], "kcal": item["kcal"]})
        total += item["kcal"]


    safety = 0
    while (kcal_target - total) > 200 and safety < 3:
        snack = _pick_item(FOODS["snack"], used)
        used.add(snack["name"])
        meals.append({"type": "snack", "name": snack["name"], "kcal": snack["kcal"]})
        total += snack["kcal"]
        safety += 1

    return {"meals": meals, "total_kcal": total, "target_kcal": kcal_target}


def generate_week_plan(profile: UserProfile) -> Dict:
    kcal = target_calories(profile)
    used: set[str] = set()

    days = []
    for _ in range(7):
        days.append(generate_day_plan(profile, kcal, used))

    return {"kcal_target": kcal, "days": days}
