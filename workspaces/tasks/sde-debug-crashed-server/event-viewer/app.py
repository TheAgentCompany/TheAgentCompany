import os
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)

# Get the database password from environment variable
db_password = os.environ.get('DB_PASSWORD', 'default_test_password')

# Configure the SQLite database, relative to the app database folder
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{basedir}/database/events.db?password={db_password}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize the database
db = SQLAlchemy(app)

# Verify the database password
def verify_db_password():
    with app.app_context():
        db.engine.connect()

verify_db_password()

# Define models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)

class Participant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)

# Create the database tables
with app.app_context():
    db.create_all()

# CRUD operations for User
@app.route('/user', methods=['POST'])
def create_user():
    data = request.json
    hashed_password = generate_password_hash(data['password'])
    new_user = User(username=data['username'], password_hash=hashed_password)
    db.session.add(new_user)
    try:
        db.session.commit()
        return jsonify({"message": "User created successfully"}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "Username already exists"}), 400

@app.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({"message": "User not found"}), 404
    return jsonify({"id": user.id, "username": user.username})

@app.route('/user/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({"message": "User not found"}), 404
    data = request.json
    user.username = data.get('username', user.username)
    if 'password' in data:
        user.password_hash = generate_password_hash(data['password'])
    db.session.commit()
    return jsonify({"message": "User updated successfully"})

@app.route('/user/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        return jsonify({"message": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"})

# CRUD operations for Event
@app.route('/event', methods=['POST'])
def create_event():
    data = request.json
    new_event = Event(name=data['name'], description=data.get('description', ''))
    db.session.add(new_event)
    db.session.commit()
    return jsonify({"message": "Event created successfully", "id": new_event.id}), 201

@app.route('/event/<int:event_id>', methods=['GET'])
def get_event(event_id):
    event = db.session.get(Event, event_id)
    if event is None:
        return jsonify({"message": "Event not found"}), 404
    return jsonify({"id": event.id, "name": event.name, "description": event.description})

@app.route('/event/<int:event_id>', methods=['PUT'])
def update_event(event_id):
    event = db.session.get(Event, event_id)
    if event is None:
        return jsonify({"message": "Event not found"}), 404
    data = request.json
    event.name = data.get('name', event.name)
    event.description = data.get('description', event.description)
    db.session.commit()
    return jsonify({"message": "Event updated successfully"})

@app.route('/event/<int:event_id>', methods=['DELETE'])
def delete_event(event_id):
    event = db.session.get(Event, event_id)
    if event is None:
        return jsonify({"message": "Event not found"}), 404
    db.session.delete(event)
    db.session.commit()
    return jsonify({"message": "Event deleted successfully"})

# CRUD operations for Participant
@app.route('/participant', methods=['POST'])
def create_participant():
    data = request.json
    new_participant = Participant(user_id=data['user_id'], event_id=data['event_id'])
    db.session.add(new_participant)
    try:
        db.session.commit()
        return jsonify({"message": "Participant added successfully", "id": new_participant.id}), 201
    except IntegrityError:
        db.session.rollback()
        return jsonify({"message": "User or Event not found"}), 400

@app.route('/participant/<int:participant_id>', methods=['GET'])
def get_participant(participant_id):
    participant = db.session.get(Participant, participant_id)
    if participant is None:
        return jsonify({"message": "Participant not found"}), 404
    return jsonify({"id": participant.id, "user_id": participant.user_id, "event_id": participant.event_id})

@app.route('/participant/<int:participant_id>', methods=['DELETE'])
def delete_participant(participant_id):
    participant = db.session.get(Participant, participant_id)
    if participant is None:
        return jsonify({"message": "Participant not found"}), 404
    db.session.delete(participant)
    db.session.commit()
    return jsonify({"message": "Participant removed successfully"})

# Get all users
@app.route('/users', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([{"id": user.id, "username": user.username} for user in users])

# Get all events
@app.route('/events', methods=['GET'])
def get_all_events():
    events = Event.query.all()
    return jsonify([{"id": event.id, "name": event.name, "description": event.description} for event in events])

# Get all participants
@app.route('/participants', methods=['GET'])
def get_all_participants():
    participants = Participant.query.all()
    return jsonify([{"id": participant.id, "user_id": participant.user_id, "event_id": participant.event_id} for participant in participants])

if __name__ == '__main__':
    app.run(debug=True)
