
import os
from flask import Flask, request, jsonify
import duckdb
from werkzeug.security import generate_password_hash, check_password_hash
from cryptography.fernet import Fernet

app = Flask(__name__)

DATABASE_DIR = os.path.join(os.path.dirname(__file__), 'database')
os.makedirs(DATABASE_DIR, exist_ok=True)
DATABASE = os.path.join(DATABASE_DIR, 'events.parquet')
ENCRYPTION_KEY_FILE = os.path.join(DATABASE_DIR, 'encryption_key.key')

if os.path.exists(ENCRYPTION_KEY_FILE):
    with open(ENCRYPTION_KEY_FILE, 'rb') as key_file:
        ENCRYPTION_KEY = key_file.read()
else:
    ENCRYPTION_KEY = Fernet.generate_key()
    with open(ENCRYPTION_KEY_FILE, 'wb') as key_file:
        key_file.write(ENCRYPTION_KEY)

cipher_suite = Fernet(ENCRYPTION_KEY)

def get_db(custom_key=None):
    global cipher_suite
    if custom_key:
        try:
            # Try to create a new Fernet instance with the custom key
            test_cipher = Fernet(custom_key)
            # Test decryption with the new key
            test_data = cipher_suite.encrypt(b"test")
            test_cipher.decrypt(test_data)
            # If successful, update the global cipher_suite
            cipher_suite = test_cipher
        except Exception:
            raise ValueError("Invalid encryption key")

    if os.path.exists(DATABASE):
        os.remove(DATABASE)
    conn = duckdb.connect(DATABASE)
    conn.execute("CREATE SEQUENCE IF NOT EXISTS event_id_seq")
    conn.execute("CREATE SEQUENCE IF NOT EXISTS user_id_seq")
    conn.execute("CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY DEFAULT nextval('event_id_seq'), name VARCHAR, date DATE, description VARCHAR)")
    conn.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY DEFAULT nextval('user_id_seq'), username VARCHAR, email VARCHAR, password VARCHAR)")
    
    return conn

def encrypt_data(data):
    return cipher_suite.encrypt(data.encode()).decode()

def decrypt_data(data):
    return cipher_suite.decrypt(data.encode()).decode()

@app.before_request
def before_request():
    get_db()  # Ensure tables are created

def save_to_parquet():
    conn = get_db()
    conn.execute(f"EXPORT DATABASE '{DATABASE_DIR}' (FORMAT PARQUET)")
    conn.close()

@app.teardown_appcontext
def close_connection(exception):
    save_to_parquet()

# Event CRUD operations
@app.route('/events', methods=['POST'])
def create_event():
    data = request.json
    db = get_db()
    encrypted_description = encrypt_data(data['description'])
    result = db.execute('INSERT INTO events (name, date, description) VALUES (?, ?, ?) RETURNING id',
               (data['name'], data['date'], encrypted_description)).fetchone()
    db.commit()
    return jsonify({'message': 'Event created successfully', 'id': result[0]}), 201

@app.route('/events', methods=['GET'])
def get_events():
    db = get_db()
    events = db.execute('SELECT * FROM events').fetchall()
    decrypted_events = []
    for event in events:
        event_dict = {
            'id': event[0],
            'name': event[1],
            'date': event[2],
            'description': decrypt_data(event[3])
        }
        decrypted_events.append(event_dict)
    return jsonify(decrypted_events)

@app.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    db = get_db()
    event = db.execute('SELECT * FROM events WHERE id = ?', (event_id,)).fetchone()
    if event is None:
        return jsonify({'error': 'Event not found'}), 404
    event_dict = dict(event)
    event_dict['description'] = decrypt_data(event_dict['description'])
    return jsonify(event_dict)

@app.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    data = request.json
    db = get_db()
    encrypted_description = encrypt_data(data['description'])
    db.execute('UPDATE events SET name = ?, date = ?, description = ? WHERE id = ?',
               (data['name'], data['date'], encrypted_description, event_id))
    db.commit()
    return jsonify({'message': 'Event updated successfully'})

@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    db = get_db()
    db.execute('DELETE FROM events WHERE id = ?', (event_id,))
    db.commit()
    return jsonify({'message': 'Event deleted successfully'})

# User CRUD operations
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    db = get_db()
    hashed_password = generate_password_hash(data['password'])
    encrypted_email = encrypt_data(data['email'])
    result = db.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?) RETURNING id',
               (data['username'], encrypted_email, hashed_password)).fetchone()
    db.commit()
    return jsonify({'message': 'User created successfully', 'id': result[0]}), 201

@app.route('/users', methods=['GET'])
def get_users():
    db = get_db()
    users = db.execute('SELECT id, username, email FROM users').fetchall()
    decrypted_users = []
    for user in users:
        user_dict = dict(user)
        user_dict['email'] = decrypt_data(user_dict['email'])
        decrypted_users.append(user_dict)
    return jsonify(decrypted_users)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    db = get_db()
    user = db.execute('SELECT id, username, email FROM users WHERE id = ?', (user_id,)).fetchone()
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    user_dict = dict(user)
    user_dict['email'] = decrypt_data(user_dict['email'])
    return jsonify(user_dict)

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    db = get_db()
    encrypted_email = encrypt_data(data['email'])
    if 'password' in data:
        hashed_password = generate_password_hash(data['password'])
        db.execute('UPDATE users SET username = ?, email = ?, password = ? WHERE id = ?',
                   (data['username'], encrypted_email, hashed_password, user_id))
    else:
        db.execute('UPDATE users SET username = ?, email = ? WHERE id = ?',
                   (data['username'], encrypted_email, user_id))
    db.commit()
    return jsonify({'message': 'User updated successfully'})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db = get_db()
    db.execute('DELETE FROM users WHERE id = ?', (user_id,))
    db.commit()
    return jsonify({'message': 'User deleted successfully'})

# Participant CRUD operations
@app.route('/participants', methods=['POST'])
def create_participant():
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO participants (user_id, event_id) VALUES (?, ?)',
                   (data['user_id'], data['event_id']))
    db.commit()
    return jsonify({'id': cursor.lastrowid}), 201

@app.route('/participants', methods=['GET'])
def get_participants():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM participants')
    participants = [dict(row) for row in cursor.fetchall()]
    return jsonify(participants)

@app.route('/participants/<int:participant_id>', methods=['GET'])
def get_participant(participant_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM participants WHERE id = ?', (participant_id,))
    participant = cursor.fetchone()
    if participant is None:
        return jsonify({'error': 'Participant not found'}), 404
    return jsonify(dict(participant))

@app.route('/participants/<int:participant_id>', methods=['PUT'])
def update_participant(participant_id):
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE participants SET user_id = ?, event_id = ? WHERE id = ?',
                   (data['user_id'], data['event_id'], participant_id))
    db.commit()
    return jsonify({'message': 'Participant updated successfully'})

@app.route('/participants/<int:participant_id>', methods=['DELETE'])
def delete_participant(participant_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM participants WHERE id = ?', (participant_id,))
    db.commit()
    return jsonify({'message': 'Participant deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
