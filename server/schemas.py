from marshmallow import Schema, fields, validate

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, error="Exercise name cannot be empty."))
    category = fields.Str(required=True)
    equipment_needed = fields.Bool(load_default=False)

    class Meta:
        ordered = True

class WorkoutSchema(Schema):
    id = fields.Int(dump_only=True)
    date = fields.Date(required=True)
    duration_minutes = fields.Int(required=True, validate=validate.Range(min=1, error="Duration must be at least 1 minute."))
    notes = fields.Str(allow_none=True)

    class Meta:
        ordered = True

class WorkoutExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    workout_id = fields.Int(required=True)
    exercise_id = fields.Int(required=True)
    sets = fields.Int(allow_none=True, validate=validate.Range(min=1))
    reps = fields.Int(allow_none=True, validate=validate.Range(min=1))
    duration_seconds = fields.Int(allow_none=True, validate=validate.Range(min=1))

    class Meta:
        ordered = True