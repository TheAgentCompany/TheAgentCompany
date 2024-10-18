import sys
from app import app, db, User, Event, Participant
from werkzeug.security import generate_password_hash
from faker import Faker
import random

fake = Faker()

def populate_database():
    with app.app_context():
        # Create users
        users = []
        for _ in range(10):
            user = User(username=fake.user_name(), password_hash=generate_password_hash(fake.password()))
            db.session.add(user)
            db.session.flush()  # Flush to get the user ID
            users.append(user)

        # Create events
        events = []
        for _ in range(5):
            event = Event(name=fake.catch_phrase(), description=fake.text())
            db.session.add(event)
            db.session.flush()  # Flush to get the event ID
            events.append(event)

        # Create participants
        for _ in range(15):
            user = random.choice(users)
            event = random.choice(events)
            participant = Participant(user_id=user.id, event_id=event.id)
            db.session.add(participant)

        db.session.commit()
        print("Database populated successfully!")

if __name__ == '__main__':
    populate_database()
