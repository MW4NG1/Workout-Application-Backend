from marshmallow import Schema, fields, validate

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100, error="Exercise name must be between 1 and 100 characters."))
    category = fields.Str(required=True, validate=validate.OneOf(["Strength", "Cardio", "Flexibility", "Calisthenics"], error="Invalid category. Choose from Strength, Cardio, Flexibility, or Calisthenics."))
    equipment_needed = fields.Bool(load_default=False)
    class Meta:
        ordered = True

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1, max=1440, error="Duration must be between 1 and 1440 minutes."))
    notes = fields.Str(allow_none=True, validate=validate.Length(max=500, error="Notes cannot exceed 500 characters."))
    class Meta:
        ordered = True

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    sets = fields.Int(allow_none=True, validate=validate.Range(min=1, max=100))
    reps = fields.Int(allow_none=True, validate=validate.Range(min=1, max=1000))
    duration_seconds = fields.Int(allow_none=True, validate=validate.Range(min=1, max=86400))
    class Meta:
        ordered = True