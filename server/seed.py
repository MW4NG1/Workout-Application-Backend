from server.config import app, db
from server.models import Exercise, Workout, WorkoutExercise

with app.app_context():
    print("Deleting existing data...")
    WorkoutExercise.query.delete()
    Workout.query.delete()
    Exercise.query.delete()

    print("Creating exercises...")
    ex1 = Exercise(name="Barbell Squat", category="Strength", equipment_needed=True)
    ex2 = Exercise(name="Push-up", category="Calisthenics", equipment_needed=False)
    ex3 = Exercise(name="Running", category="Cardio", equipment_needed=False)
    db.session.add_all([ex1, ex2, ex3])
    db.session.commit()

    print("Creating workouts...")
    w1 = Workout(date="2026-10-26", duration_minutes=45, notes="Leg day focus")
    w2 = Workout(date="2026-10-27", duration_minutes=30, notes="Morning cardio & core")
    db.session.add_all([w1, w2])
    db.session.commit()

    print("Linking exercises to workouts...")
    we1 = WorkoutExercise(workout_id=w1.id, exercise_id=ex1.id, sets=4, reps=10)
    we2 = WorkoutExercise(workout_id=w1.id, exercise_id=ex2.id, sets=3, reps=15)
    we3 = WorkoutExercise(workout_id=w2.id, exercise_id=ex3.id, duration_seconds=1800)
    db.session.add_all([we1, we2, we3])
    db.session.commit()

    print("Seeding complete!")