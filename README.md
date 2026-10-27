# Workout Application Backend

A robust RESTful API built with Flask, SQLAlchemy, and Marshmallow designed to manage workouts, exercises, and their relationships with request and response validation.

## Project Description

This backend application provides a complete system for tracking fitness routines.It supports full CRUD functionality for exercises and workouts, handles relational tracking of exercise parameters via a join table and enforces strict data integrity using Marshmallow schema validation and database-level constraints.

## Project Structure

Workout-Application-Backend/
├── instance/
│ └── app.db
├── migrations/
│ ├── versions/
│ ├── alembic.ini
│ ├── env.py
│ └── script.py.mako
├── server/
│ ├── __init__.py
│ ├── app.py
│ ├── config.py
│ ├── models.py
│ ├── schemas.py
│ └── seed.py
├── Pipfile
├── Pipfile.lock
└── README.md

## Tech Stack

- Python
- Flask & Flask-Migrate (Alembic)
- Flask-SQLAlchemy
- Marshmallow
- SQLite

## Installation Instructions

1. Clone the repository:
   git clone <Workout-Application-Backend>
   cd Workout-Application-Backend

2. Install Dependacies
   pipenv install

3. Activate the virtual environment
   pipenv shell

4. Run database migrations to set up the SQLite database
   flask db upgrade

5. Seed the database with initial sample data
   python server/seed.py

## Run Instructions

- Start the development server
  python server/app.py

## API Endpoints

1. Exercises

- GET /exercises
  Description: Retrieves a list of all available exercises.
- POST /exercises
  Description: Creates a new exercise. Requires name, category, and optional equipment_needed flag in the request body.
- GET /exercises/<id>
  Description: Retrieves details for a specific exercise by ID, including associated workouts.
- DELETE /exercises/<id>
  Description: Deletes a specific exercise by ID along with its associated workout exercise records.

2. Workouts

- GET /workouts
  Description: Retrieves a list of all logged workouts.
- POST /workouts
  Description: Creates a new workout session. Requires date, duration_minutes, and optional notes.
- GET /workouts/<id>
  Description: Retrieves details for a specific workout by ID, including all attached exercises and set/rep metrics.
- DELETE /workouts/<id>
  Description: Deletes a specific workout by ID along with its associated workout exercise records.

3. Workout Exercises (Join Table)

- POST /workouts/<workout_id>/exercises/<exercise_id>/workout_exercises
  Description: Links an exercise to a specific workout with performance metrics
