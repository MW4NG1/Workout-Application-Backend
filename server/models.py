from server.config import db
from sqlalchemy.orm import validates
from sqlalchemy import CheckConstraint

class Exercise(db.Model):
    __tablename__ = 'exercises'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    category = db.Column(db.String, nullable=False)
    equipment_needed = db.Column(db.Boolean, nullable=False, default=False)
    # Relationships
    workout_exercises = db.relationship('WorkoutExercise', back_populates='exercise', cascade='all, delete-orphan')
    workouts = db.relationship('Workout', secondary='workout_exercises', back_populates='exercises')

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


class Workout(db.Model):
    __tablename__ = 'workouts'

    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String, nullable=False)
    duration_minutes = db.Column(db.Integer, nullable=False)
    notes = db.Column(db.Text, nullable=True)

    __table_args__ = (
        CheckConstraint('duration_minutes > 0', name='check_duration_positive'),
    )
    # Relationships
    workout_exercises = db.relationship('WorkoutExercise', back_populates='workout', cascade='all, delete-orphan')
    exercises = db.relationship('Exercise', secondary='workout_exercises', back_populates='workouts')

    @validates('duration_minutes')
    def validate_duration(self, key, duration):
        if duration is None or duration <= 0:
            raise ValueError("Workout duration must be greater than 0 minutes.")
        return duration


class WorkoutExercise(db.Model):
    __tablename__ = 'workout_exercises'

    id = db.Column(db.Integer, primary_key=True)
    workout_id = db.Column(db.Integer, db.ForeignKey('workouts.id'), nullable=False)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercises.id'), nullable=False)
    reps = db.Column(db.Integer, nullable=True)
    sets = db.Column(db.Integer, nullable=True)
    duration_seconds = db.Column(db.Integer, nullable=True)

    __table_args__ = (
        CheckConstraint('sets IS NULL OR sets > 0', name='check_sets_positive'),
        CheckConstraint('reps IS NULL OR reps > 0', name='check_reps_positive'),
    )
    # Relationships
    workout = db.relationship('Workout', back_populates='workout_exercises')
    exercise = db.relationship('Exercise', back_populates='workout_exercises')

    @validates('sets')
    def validate_sets(self, key, sets):
        if sets is not None and sets <= 0:
            raise ValueError("Sets must be greater than zero if provided.")
        return sets

    @validates('reps')
    def validate_reps(self, key, reps):
        if reps is not None and reps <= 0:
            raise ValueError("Reps must be greater than zero if provided.")
        return reps

