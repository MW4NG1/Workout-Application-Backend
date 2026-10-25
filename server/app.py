from flask import request, jsonify
from server.config import app, db, ma
from server.models import Exercise, Workout, WorkoutExercise
from marshmallow import fields, validate, ValidationError

