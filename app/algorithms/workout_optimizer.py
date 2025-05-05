"""
Advanced workout optimization algorithm module.

Implements a multi-criteria optimization algorithm for generating optimal
workout plans based on user goals, fitness level, and available time.
Uses a combination of knapsack algorithm and muscle group balancing.
"""

from typing import List
from sqlalchemy.orm import Session
from app.schemas.workout import WorkoutPlan, WorkoutOptimizationParams
from app.models.user import User as DBUser
from app.models.exercise import Exercise
import numpy as np
from collections import defaultdict


def optimize_workout_plan(
        db: Session,
        params: WorkoutOptimizationParams,
        user: DBUser
) -> WorkoutPlan:
    """
    Optimize workout plan using advanced multi-criteria optimization.

    Args:
        db: Database session
        params: Workout optimization parameters
        user: User object with fitness level and preferences

    Returns:
        WorkoutPlan: Optimized workout plan

    Algorithm:
        1. Filters exercises by user criteria
        2. Scores each exercise based on multiple factors
        3. Uses modified knapsack algorithm with muscle group balancing
        4. Optimizes exercise order for maximum efficiency
    """
    # 1. Get and filter exercises
    exercises = db.query(Exercise).all()
    exercises = _filter_exercises(exercises, params, user)

    # 2. Score exercises based on multiple criteria
    scored_exercises = _score_exercises(exercises, params, user)

    # 3. Optimize selection using modified knapsack algorithm
    selected_exercises = _optimize_selection(scored_exercises, params.available_time)

    # 4. Optimize exercise order
    optimized_order = _optimize_order(selected_exercises)

    # 5. Calculate plan metrics
    return _build_workout_plan(optimized_order)


def _filter_exercises(
        exercises: List[Exercise],
        params: WorkoutOptimizationParams,
        user: DBUser
) -> List[Exercise]:
    """Filter exercises based on user criteria"""
    filtered = []

    for ex in exercises:
        # Filter by goal
        if params.goal == "weight_loss" and ex.calories_burned < 5:
            continue
        if params.goal == "muscle_gain" and ex.muscle_group not in params.target_muscles:
            continue
        if params.goal == "endurance" and not ex.is_cardio:
            continue

        # Filter by fitness level
        if user.fitness_level == "beginner" and ex.difficulty > 3:
            continue
        if user.fitness_level == "intermediate" and ex.difficulty > 7:
            continue

        filtered.append(ex)

    return filtered


def _score_exercises(
        exercises: List[Exercise],
        params: WorkoutOptimizationParams,
        user: DBUser
) -> List[tuple]:
    """Score each exercise based on multiple criteria"""
    scored = []

    for ex in exercises:
        score = 0

        # Goal scoring
        if params.goal == "weight_loss":
            score += ex.calories_burned * 0.7
        elif params.goal == "muscle_gain":
            score += ex.difficulty * 0.5
            if ex.muscle_group in params.target_muscles:
                score += 0.5
        elif params.goal == "endurance":
            score += ex.duration * 0.3 + ex.calories_burned * 0.7

        # User preference scoring
        if ex.equipment in user.preferred_equipment:
            score += 0.2
        if ex.muscle_group in user.favorite_muscle_groups:
            score += 0.3

        scored.append((score, ex))

    return scored


def _optimize_selection(
        scored_exercises: List[tuple],
        available_time: int
) -> List[Exercise]:
    """Modified knapsack algorithm with muscle group balancing"""
    # Sort by score/duration ratio
    scored_exercises.sort(key=lambda x: x[0] / x[1].avg_duration, reverse=True)

    selected = []
    total_time = 0
    muscle_group_counts = defaultdict(int)

    for score, ex in scored_exercises:
        if total_time + ex.avg_duration > available_time:
            continue

        # Muscle group balancing
        if muscle_group_counts[ex.muscle_group] >= 2:  # Max 2 per muscle group
            continue

        selected.append(ex)
        total_time += ex.avg_duration
        muscle_group_counts[ex.muscle_group] += 1

        if total_time >= available_time * 0.9:  # 90% of time is good enough
            break

    return selected


def _optimize_order(exercises: List[Exercise]) -> List[Exercise]:
    """Optimize exercise order to alternate muscle groups"""
    if not exercises:
        return []

    # Group by muscle group
    muscle_groups = defaultdict(list)
    for ex in exercises:
        muscle_groups[ex.muscle_group].append(ex)

    # Create balanced order
    ordered = []
    while muscle_groups:
        for mg in list(muscle_groups.keys()):
            if muscle_groups[mg]:
                ordered.append(muscle_groups[mg].pop())
            else:
                del muscle_groups[mg]

    return ordered


def _build_workout_plan(exercises: List[Exercise]) -> WorkoutPlan:
    """Build final workout plan with metrics"""
    if not exercises:
        return WorkoutPlan(exercises=[], total_duration=0, estimated_calories=0, difficulty=0)

    total_duration = sum(ex.avg_duration for ex in exercises)
    total_calories = sum(ex.calories_burned for ex in exercises)
    avg_difficulty = sum(ex.difficulty for ex in exercises) / len(exercises)

    return WorkoutPlan(
        exercises=[{"id": ex.id, "name": ex.name} for ex in exercises],
        total_duration=total_duration,
        estimated_calories=total_calories,
        difficulty=round(avg_difficulty, 1),
        muscle_group_balance=_calculate_muscle_balance(exercises)
    )


def _calculate_muscle_balance(exercises: List[Exercise]) -> dict:
    """Calculate muscle group balance score"""
    muscle_counts = defaultdict(int)
    for ex in exercises:
        muscle_counts[ex.muscle_group] += 1

    total = len(exercises)
    if total == 0:
        return {}

    return {mg: round(count / total, 2) for mg, count in muscle_counts.items()}