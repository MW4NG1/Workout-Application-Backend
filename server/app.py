from flask import request, jsonify
from server.config import app, db, ma
from server.models import Exercise, Workout, WorkoutExercise
from marshmallow import fields, validate, ValidationError

class ExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Exercise
        load_instance = True
        include_relationships = True

    name = fields.String(required=True, validate=validate.Length(min=1, error="Exercise name cannot be blank."))
    category = fields.String(required=True, validate=validate.Length(min=1, error="Category cannot be blank."))

class WorkoutExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = WorkoutExercise
        load_instance = True
        include_fk = True

    sets = fields.Integer(allow_none=True, validate=validate.Range(min=1, error="Sets must be greater than 0"))
    reps = fields.Integer(allow_none=True, validate=validate.Range(min=1, error="Reps must be greater than 0"))
    duration_seconds = fields.Integer(allow_none=True, validate=validate.Range(min=0))

    exercise = fields.Nested(ExerciseSchema, dump_only=True)

class WorkoutSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Workout
        load_instance = True
        include_relationships = True

    date = fields.String(required=True, validate=validate.Length(min=1))
    duration_minutes = fields.Integer(required=True, validate=validate.Range(min=1, error="Duration must be greater than 0."))
    workout_exercises = fields.Nested(WorkoutExerciseSchema, many=True, dump_only=True)

exercise_schema = ExerciseSchema()
exercises_schema = ExerciseSchema(many=True)
workout_schema = WorkoutSchema()
workouts_schema = WorkoutSchema(many=True)
workout_exercise_schema = WorkoutExerciseSchema()

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Workout Application Backend API!"})

# --- Exercise Endpoints ---
@app.route('/exercises', methods=['GET'])
def get_exercises():
    exercises = Exercise.query.all()
    return exercises_schema.dump(exercises), 200

@app.route('/exercises', methods=['POST'])
def create_exercise():
    data = request.get_json()
    try:
        validated_data = exercise_schema.load(data)
        db.session.add(validated_data)
        db.session.commit()
        return exercise_schema.dump(validated_data), 201
    except ValidationError as err:
        return {"errors": err.messages}, 400
    except Exception as e:
        return {"error": str(e)}, 400

@app.route('/exercises/<int:id>', methods=['DELETE'])
def delete_exercise(id):
    exercise = Exercise.query.get(id)
    if not exercise:
        return {"error": "Exercise not found"}, 404
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
    return workout_schema.dump(workout), 200

@app.route('/workouts', methods=['POST'])
def create_workout():
    data = request.get_json()
    try:
        validated_data = workout_schema.load(data)
        workout = Workout(
            date=validated_data.get('date'),
            duration_minutes=validated_data.get('duration_minutes'),
            notes=validated_data.get('notes')
        )
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
    db.session.delete(workout)
    db.session.commit()
    return {}, 204

@app.route('/workout_exercises', methods=['POST'])
def add_exercise_to_workout():
    data = request.get_json()
    try:
        validated_data = workout_exercise_schema.load(data)
        db.session.add(validated_data)
        db.session.commit()
        return workout_exercise_schema.dump(validated_data), 201
    except ValidationError as err:
        return {"errors": err.messages}, 400
    except Exception as e:
        return {"error": str(e)}, 400

if __name__ == '__main__':
    app.run(port=5555, debug=True)