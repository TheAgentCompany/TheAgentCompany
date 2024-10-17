# Event Viewer Application

The Event Viewer is a Flask-based web application that manages events, users, and participants. It provides a RESTful API for creating, reading, updating, and deleting (CRUD) events, users, and participants.

## Features

- CRUD operations for events, users, and participants
- SQLite database with password protection
- Fake data generation for testing and development
- Unit tests to ensure functionality

## Requirements

- Python 3.7+
- Flask
- Werkzeug
- Faker

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/event-viewer.git
   cd event-viewer
   ```

2. Install the required packages:

   ```bash
   apt install sqlcipher
   pip install -r requirements.txt
   ```

## Usage

1. Run the Flask application:

   ```bash
   python app.py
   ```

2. The application will be available at `http://localhost:5000`

## API Endpoints

### Events

- GET /events - List all events
- POST /events - Create a new event
- GET /events/{id} - Get a specific event
- PUT /events/{id} - Update a specific event
- DELETE /events/{id} - Delete a specific event

### Users

- GET /users - List all users
- POST /users - Create a new user
- GET /users/{id} - Get a specific user
- PUT /users/{id} - Update a specific user
- DELETE /users/{id} - Delete a specific user

### Participants

- GET /participants - List all participants
- POST /participants - Create a new participant
- GET /participants/{id} - Get a specific participant
- PUT /participants/{id} - Update a specific participant
- DELETE /participants/{id} - Delete a specific participant

## Testing

Run the unit tests:

```bash
python test_app.py
```

## Security

The application uses a SQLite database with password protection. The database password is set in `app.py`. Make sure to change the default password in a production environment.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
