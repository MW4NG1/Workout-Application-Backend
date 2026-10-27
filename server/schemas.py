from marshmallow import Schema, fields, validate

class ExerciseSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True, validate=validate.Length(min=1, error="Exercise name cannot be empty."))
    category = fields.Str(required=True)
    equipment_needed = fields.Bool(load_default=False)

    class Meta:
        ordered = True

