
# Event Viewer

This is a FastAPI server that implements CRUD operations for an event viewer, using DuckDB with encrypted parquet files for data storage.

## Setup

1. Clone this repository.
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Set the `DB_PASSWORD` environment variable:
   ```
   export DB_PASSWORD=$(python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())")
   ```

## Populating the Database

To populate the database with fake data, run:

```
python populate_db.py
```

This will create encrypted parquet files in the `database/` directory.

## Running the Server

To start the server, run:

```
python main.py
```

The server will start on `http://localhost:5000`.

## API Endpoints

### Users

- GET /users - List all users
- POST /users - Create a new user
- PUT /users/{user_id} - Update a user
- DELETE /users/{user_id} - Delete a user

### Events

- GET /events - List all events
- POST /events - Create a new event
- PUT /events/{event_id} - Update an event
- DELETE /events/{event_id} - Delete an event

### Participants

- GET /participants - List all participants
- POST /participants - Create a new participant
- PUT /participants/{participant_id} - Update a participant
- DELETE /participants/{participant_id} - Delete a participant


## Security

The database files are encrypted using Fernet symmetric encryption. The encryption key is stored in the `DB_PASSWORD` environment variable.
