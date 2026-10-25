from server.config import db
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint

class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)

    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')

    @validates('name')
    def validate_name(self, key, name):
        if not name or not name.strip():
            raise ValueError("Exercise name cannot be empty.")
        return name.strip()

    @validates('category')
    def validate_category(self, key, category):
        if not category or not category.strip():
            raise ValueError("Exercise category cannot be empty.")
        return category.strip()