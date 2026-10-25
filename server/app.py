from flask import request, jsonify
from server.config import app, db, ma
from server.models import Exercise, Workout, WorkoutExercise
from marshmallow import fields, validate, ValidationError

class ExerciseSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Exercise
        load_instance = True
    
    name = fields.String(required=True, validate=validate.Length(min=1, error="Exercise name cannot be blank."))
    category = fields.String(required=True, validate=validate.Length(min=1, error="Category cannot be blank."))

class WorkoutSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    date = fields.String(required=True, validate=validate.Length(min=1))
    duration_minutes = fields.Integer(required=True, validate=validate.Range(min=1, error="Duration must be greater than 0."))
    notes = fields.String()
    class Meta:
        fields = ("id", "date", "duration_minutes", "notes", "workout_exercises")

class WorkoutExerciseSchema(ma.Schema):
    id = fields.Integer(dump_only=True)
    workout_id = fields.Integer(required=True)
    exercise_id = fields.Integer(required=True)
    sets = fields.Integer(allow_none=True, validate=validate.Range(min=1, error="Sets must be greater than 0"))
    reps = fields.Integer(allow_none=True, validate=validate.Range(min=1, error="Reps must be greater than 0"))
    duration_seconds = fields.Integer(allow_none=True, validate=validate.Range(min=0))

    class Meta:
        fields = ("id", "workout_id", "exercise_id", "sets", "reps", "duration_seconds", "exercise")
        load_instance = True

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