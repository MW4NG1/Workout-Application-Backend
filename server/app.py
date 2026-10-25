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