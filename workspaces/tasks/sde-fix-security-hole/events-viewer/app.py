
import os
from flask import Flask, request, jsonify
import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

DATABASE = 'events.db'
DB_PASSWORD = os.getenv('DB_PASSWORD', 'cat123')  # Default password for development

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

@app.before_request
def before_request():
    db = get_db()
    db.execute(f"PRAGMA key='{DB_PASSWORD}'")

# Event CRUD operations
@app.route('/events', methods=['POST'])
def create_event():
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute('INSERT INTO events (name, date, description) VALUES (?, ?, ?)',
                   (data['name'], data['date'], data['description']))
    db.commit()
    return jsonify({'id': cursor.lastrowid}), 201

@app.route('/events', methods=['GET'])
def get_events():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM events')
    events = [dict(row) for row in cursor.fetchall()]
    return jsonify(events)

@app.route('/events/<int:event_id>', methods=['GET'])
def get_event(event_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT * FROM events WHERE id = ?', (event_id,))
    event = cursor.fetchone()
    if event is None:
        return jsonify({'error': 'Event not found'}), 404
    return jsonify(dict(event))

@app.route('/events/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    data = request.json
    db = get_db()
    cursor = db.cursor()
    cursor.execute('UPDATE events SET name = ?, date = ?, description = ? WHERE id = ?',
                   (data['name'], data['date'], data['description'], event_id))
    db.commit()
    return jsonify({'message': 'Event updated successfully'})

@app.route('/events/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM events WHERE id = ?', (event_id,))
    db.commit()
    return jsonify({'message': 'Event deleted successfully'})

# User CRUD operations
@app.route('/users', methods=['POST'])
def create_user():
    data = request.json
    db = get_db()
    cursor = db.cursor()
    hashed_password = generate_password_hash(data['password'])
    cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                   (data['username'], data['email'], hashed_password))
    db.commit()
    return jsonify({'id': cursor.lastrowid}), 201

@app.route('/users', methods=['GET'])
def get_users():
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id, username, email FROM users')
    users = [dict(row) for row in cursor.fetchall()]
    return jsonify(users)

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('SELECT id, username, email FROM users WHERE id = ?', (user_id,))
    user = cursor.fetchone()
    if user is None:
        return jsonify({'error': 'User not found'}), 404
    return jsonify(dict(user))

@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    db = get_db()
    cursor = db.cursor()
    if 'password' in data:
        hashed_password = generate_password_hash(data['password'])
        cursor.execute('UPDATE users SET username = ?, email = ?, password = ? WHERE id = ?',
                       (data['username'], data['email'], hashed_password, user_id))
    else:
        cursor.execute('UPDATE users SET username = ?, email = ? WHERE id = ?',
                       (data['username'], data['email'], user_id))
    db.commit()
    return jsonify({'message': 'User updated successfully'})

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    db = get_db()
    cursor = db.cursor()
    cursor.execute('DELETE FROM users WHERE id = ?', (user_id,))
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
