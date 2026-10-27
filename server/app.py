from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from server.models import db, Exercise, Workout, WorkoutExercise
from marshmallow import fields, validate, ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)
db.init_app(app)

# Routes
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Workout Application Backend API!"})

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return [
        {
            "id": e.id,
            "name": e.name,
            "category": e.category,
            "equipment_needed": e.equipment_needed
        } for e in exercises
    ], 200

@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return {"error": "Exercise not found"}, 404
    return {
        "id": exercise.id,
        "name": exercise.name,
        "category": exercise.category,
        "equipment_needed": exercise.equipment_needed,
        "workouts": [
            {
                "id": w.id,
                "date": str(w.date),
                "duration_minutes": w.duration_minutes,
                "notes": w.notes
            } for w in exercise.workouts
        ]
    }, 200

@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()
    try:
        exercise = Exercise(
            name=data.get('name'),
            category=data.get('category'),
            equipment_needed=data.get('equipment_needed', False)
        )
        db.session.add(exercise)
        db.session.commit()
        return {
            "id": exercise.id,
            "name": exercise.name,
            "category": exercise.category,
            "equipment_needed": exercise.equipment_needed
        }, 201
    except Exception as e:
        return {"error": str(e)}, 400

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return {"error": "Exercise not found"}, 404
        
    for we in exercise.workout_exercises:
        db.session.delete(we)
    db.session.delete(exercise)
    db.session.commit()
    return {}, 204

@app.route('/workouts', methods=['GET'])
def get_workouts():
    workouts = Workout.query.all()
    return [
        {
            "id": w.id,
            "date": str(w.date),
            "duration_minutes": w.duration_minutes,
            "notes": w.notes
        } for w in workouts
    ], 200

@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return {"error": "Workout not found"}, 404
    return {
        "id": workout.id,
        "date": str(workout.date),
        "duration_minutes": workout.duration_minutes,
        "notes": workout.notes,
        "workout_exercises": [
            {
                "id": we.id,
                "exercise_id": we.exercise_id,
                "exercise_name": we.exercise.name,
                "reps": we.reps,
                "sets": we.sets,
                "duration_seconds": we.duration_seconds
            } for we in workout.workout_exercises
        ]
    }, 200

@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()
    try:
        workout = Workout(
            date=data.get('date'),
            duration_minutes=data.get('duration_minutes'),
            notes=data.get('notes')
        )
        db.session.add(workout)
        db.session.commit()
        return {
            "id": workout.id,
            "date": str(workout.date),
            "duration_minutes": workout.duration_minutes,
            "notes": workout.notes
        }, 201
    except Exception as e:
        return {"error": str(e)}, 400

@app.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return {"error": "Workout not found"}, 404
        
    for we in workout.workout_exercises:
        db.session.delete(we)
    db.session.delete(workout)
    db.session.commit()
    return {}, 204

@app.route('/workouts/<int:workout_id>/exercises/<int:exercise_id>/workout_exercises', methods=['POST'])
def add_exercise_to_workout(workout_id, exercise_id):
    workout = Workout.query.get(workout_id)
    exercise = Exercise.query.get(exercise_id)
    if not workout or not exercise:
        return {"error": "Workout or Exercise not found"}, 404
        
    data = request.get_json() or {}
    try:
        workout_exercise = WorkoutExercise(
            workout_id=workout_id,
            exercise_id=exercise_id,
            sets=data.get('sets'),
            reps=data.get('reps'),
            duration_seconds=data.get('duration_seconds')
        )
        db.session.add(workout_exercise)
        db.session.commit()
        return {
            "id": workout_exercise.id,
            "workout_id": workout_exercise.workout_id,
            "exercise_id": workout_exercise.exercise_id,
            "sets": workout_exercise.sets,
            "reps": workout_exercise.reps,
            "duration_seconds": workout_exercise.duration_seconds
        }, 201
    except Exception as e:
        return {"error": str(e)}, 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)