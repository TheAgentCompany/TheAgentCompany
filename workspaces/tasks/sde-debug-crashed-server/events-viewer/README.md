# Event Viewer Application

The Event Viewer is a Flask-based web application that manages events and users. It provides a RESTful API for creating, reading, updating, and deleting (CRUD) events and users.

## Features

- CRUD operations for events and users
- DuckDB database with encrypted Parquet files
- Encryption for sensitive data
- Unit tests to ensure functionality

## Requirements

- Python 3.7+
- Flask
- Werkzeug
- DuckDB
- PyArrow
- Cryptography

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/event-viewer.git
   cd event-viewer
   ```

2. Install the required packages:

   ```bash
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

## Testing

Run the unit tests:

```bash
python test_app.py
```

## Security

The application uses DuckDB with encrypted Parquet files. Sensitive data, such as event descriptions and user emails, are encrypted before being stored in the database. The encryption key is stored in a separate file and should be properly secured in a production environment.

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)

