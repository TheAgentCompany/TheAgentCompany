# Event Viewer App

This is a Flask-based web application for managing events and participants.

## Features

- User management (create, read, update, delete)
- Event management (create, read, update, delete)
- Participant management (add participants to events)

## Setup

1. Install the required packages:

   ```bash
   pip install flask flask-sqlalchemy faker
   ```

2. Set the database password as an environment variable:

   ```bash
   export DB_PASSWORD=your_password_here
   ```

3. Run the database population script:

   ```bash
   python populate_database.py
   ```

4. Start the Flask server:

   ```bash
   python app.py
   ```

## Usage

The app provides RESTful API endpoints for managing users, events, and participants. Use tools like curl or Postman to interact with the API.

Example endpoints:

- POST /user: Create a new user
- GET /user/[id]: Get user details
- POST /event: Create a new event
- GET /event/[id]: Get event details
- POST /participant: Add a participant to an event

## Testing

Run the unit tests using:

```bash
python -m unittest test_app.py
```

## Security

The app uses SQLite with encryption. Make sure to keep your DB_PASSWORD secure and don't share it publicly.
