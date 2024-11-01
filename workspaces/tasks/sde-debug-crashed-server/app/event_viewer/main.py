import os
from flask import Flask, request, jsonify
import duckdb
import pyarrow.parquet as pq
import pyarrow as pa
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import base64

app = Flask(__name__)
current_dir = os.path.dirname(os.path.abspath(__file__))

# Get the password from environment variable or use a default
DB_PASSWORD = os.environ.get("DB_PASSWORD", "default_password")

# Derive the key using HKDF
hkdf = HKDF(
    algorithm=hashes.SHA256(),
    length=32,
    salt=None,
    info=b"event_viewer_key_derivation",
)
key = base64.urlsafe_b64encode(hkdf.derive(DB_PASSWORD.encode()))

fernet = Fernet(key)

# Database connection
def get_db():
    conn = duckdb.connect(database=':memory:')
    load_data(conn)
    return conn

# Helper function to decrypt and load data
def load_encrypted_parquet(file_path):
    with open(file_path, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data = fernet.decrypt(encrypted_data)
    return pq.read_table(pa.py_buffer(decrypted_data))

# Load data into DuckDB
def load_data(conn):
    database_dir = os.path.join(current_dir, '..', 'database')
    users = load_encrypted_parquet(os.path.join(database_dir, 'users.parquet'))
    events = load_encrypted_parquet(os.path.join(database_dir, 'events.parquet'))
    participants = load_encrypted_parquet(os.path.join(database_dir, 'participants.parquet'))
    
    conn.register('users', users)
    conn.register('events', events)
    conn.register('participants', participants)

# CRUD operations for Users
@app.route("/users", methods=['GET'])
def read_users():
    db = get_db()
    result = db.execute("SELECT * FROM users").fetchall()
    db.close()
    return jsonify([{"id": row[0], "name": row[1], "email": row[2]} for row in result])

@app.route("/users", methods=['POST'])
def create_user():
    user = request.json
    db = get_db()
    db.execute(f"INSERT INTO users VALUES ({user['id']}, '{user['name']}', '{user['email']}')")
    db.close()
    return jsonify(user)

@app.route("/users/<int:user_id>", methods=['PUT'])
def update_user(user_id):
    user = request.json
    db = get_db()
    db.execute(f"UPDATE users SET name = '{user['name']}', email = '{user['email']}' WHERE id = {user_id}")
    db.close()
    return jsonify(user)

@app.route("/users/<int:user_id>", methods=['DELETE'])
def delete_user(user_id):
    db = get_db()
    db.execute(f"DELETE FROM users WHERE id = {user_id}")
    db.close()
    return jsonify({"message": "User deleted"})

# CRUD operations for Events
@app.route("/events", methods=['GET'])
def read_events():
    db = get_db()
    result = db.execute("SELECT * FROM events").fetchall()
    db.close()
    return jsonify([{"id": row[0], "name": row[1], "date": row[2]} for row in result])

@app.route("/events", methods=['POST'])
def create_event():
    event = request.json
    db = get_db()
    db.execute(f"INSERT INTO events VALUES ({event['id']}, '{event['name']}', '{event['date']}')")
    db.close()
    return jsonify(event)

@app.route("/events/<int:event_id>", methods=['PUT'])
def update_event(event_id):
    event = request.json
    db = get_db()
    db.execute(f"UPDATE events SET name = '{event['name']}', date = '{event['date']}' WHERE id = {event_id}")
    db.close()
    return jsonify(event)

@app.route("/events/<int:event_id>", methods=['DELETE'])
def delete_event(event_id):
    db = get_db()
    db.execute(f"DELETE FROM events WHERE id = {event_id}")
    db.close()
    return jsonify({"message": "Event deleted"})

# CRUD operations for Participants
@app.route("/participants", methods=['GET'])
def read_participants():
    db = get_db()
    result = db.execute("SELECT * FROM participants").fetchall()
    db.close()
    return jsonify([{"id": row[0], "user_id": row[1], "event_id": row[2]} for row in result])

@app.route("/participants", methods=['POST'])
def create_participant():
    participant = request.json
    db = get_db()
    db.execute(f"INSERT INTO participants VALUES ({participant['id']}, {participant['user_id']}, {participant['event_id']})")
    db.close()
    return jsonify(participant)

@app.route("/participants/<int:participant_id>", methods=['PUT'])
def update_participant(participant_id):
    participant = request.json
    db = get_db()
    db.execute(f"UPDATE participants SET user_id = {participant['user_id']}, event_id = {participant['event_id']} WHERE id = {participant_id}")
    db.close()
    return jsonify(participant)

@app.route("/participants/<int:participant_id>", methods=['DELETE'])
def delete_participant(participant_id):
    db = get_db()
    db.execute(f"DELETE FROM participants WHERE id = {participant_id}")
    db.close()
    return jsonify({"message": "Participant deleted"})

if __name__ == "__main__":
    app.run(debug=True)
