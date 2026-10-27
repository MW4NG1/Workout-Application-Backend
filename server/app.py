from flask import Flask, make_response, request, jsonify
from flask_migrate import Migrate
from server.models import db, Exercise, Workout, WorkoutExercise
from server.schemas import ExerciseSchema, WorkoutSchema, WorkoutExerciseSchema
from marshmallow import ValidationError

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False
migrate = Migrate(app, db)
db.init_app(app)

# Initialize Marshmallow Schemas
exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()

# Routes
@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Workout Application Backend API!"})

@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return exercises_schema.dump(exercises), 200 

@app.route('/exercises/<int:id>', methods=['GET'])
def get_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return {"error": "Exercise not found"}, 404
    result = exercise_schema.dump(exercise)
    result["workouts"] = [
        {
            "id": w.id,
            "date": str(w.date),
            "duration_minutes": w.duration_minutes,
            "notes": w.notes
        } for w in exercise.workouts
    ]
    return result, 200

@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json() or {}
    try:
        validated_data = exercise_schema.load(data)
        exercise = Exercise(**validated_data)
        db.session.add(exercise)
        db.session.commit()
        return exercise_schema.dump(exercise), 201
    except ValidationError as err:
        return {"errors": err.messages}, 400
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
    return workouts_schema.dump(workouts), 200

@app.route('/workouts/<int:id>', methods=['GET'])
def get_workout(id):
    workout = Workout.query.get(id)
    if not workout:
        return {"error": "Workout not found"}, 404
    result = workout_schema.dump(workout)
    result["workout_exercises"] = [
        {
            "id": we.id,
            "exercise_id": we.exercise_id,
            "exercise_name": we.exercise.name,
            "reps": we.reps,
            "sets": we.sets,
            "duration_seconds": we.duration_seconds
        } for we in workout.workout_exercises
    ]
    return result, 200

@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json() or {}
    try:
        validated_data = workout_schema.load(data)
        workout = Workout(**validated_data)
        db.session.add(workout)
        db.session.commit()
        return workout_schema.dump(workout), 201
    except ValidationError as err:
        return {"errors": err.messages}, 400
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
        data['workout_id'] = workout_id
        data['exercise_id'] = exercise_id
        validated_data = workout_exercise_schema.load(data)
        
        workout_exercise = WorkoutExercise(**validated_data)
        db.session.add(workout_exercise)
        db.session.commit()
        return workout_exercise_schema.dump(workout_exercise), 201
    except ValidationError as err:
        return {"errors": err.messages}, 400
    except Exception as e:
        return {"error": str(e)}, 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)