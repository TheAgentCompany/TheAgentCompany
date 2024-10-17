
import sqlite3
from werkzeug.security import generate_password_hash
from faker import Faker
import random
from datetime import datetime, timedelta

DATABASE = 'events.db'
DB_PASSWORD = 'cat123'

fake = Faker()

def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

def create_tables():
    db = get_db()
    db.execute(f"PRAGMA key='{DB_PASSWORD}'")
    
    db.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        email TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
    ''')

    db.execute('''
    CREATE TABLE IF NOT EXISTS events (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        date TEXT NOT NULL,
        description TEXT
    )
    ''')

    db.execute('''
    CREATE TABLE IF NOT EXISTS participants (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        event_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (event_id) REFERENCES events (id)
    )
    ''')

    db.commit()
    db.close()

def populate_users(num_users=10):
    db = get_db()
    db.execute(f"PRAGMA key='{DB_PASSWORD}'")

    for _ in range(num_users):
        username = fake.user_name()
        email = fake.email()
        password = generate_password_hash(fake.password())
        db.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?)',
                   (username, email, password))

    db.commit()
    db.close()

def populate_events(num_events=20):
    db = get_db()
    db.execute(f"PRAGMA key='{DB_PASSWORD}'")

    for _ in range(num_events):
        name = fake.catch_phrase()
        date = fake.date_time_between(start_date='now', end_date='+1y').strftime('%Y-%m-%d %H:%M:%S')
        description = fake.text()
        db.execute('INSERT INTO events (name, date, description) VALUES (?, ?, ?)',
                   (name, date, description))

    db.commit()
    db.close()

def populate_participants(num_participants=50):
    db = get_db()
    db.execute(f"PRAGMA key='{DB_PASSWORD}'")

    user_ids = [row['id'] for row in db.execute('SELECT id FROM users').fetchall()]
    event_ids = [row['id'] for row in db.execute('SELECT id FROM events').fetchall()]

    for _ in range(num_participants):
        user_id = random.choice(user_ids)
        event_id = random.choice(event_ids)
        db.execute('INSERT INTO participants (user_id, event_id) VALUES (?, ?)',
                   (user_id, event_id))

    db.commit()
    db.close()

if __name__ == '__main__':
    create_tables()
    populate_users()
    populate_events()
    populate_participants()
    print("Database populated successfully!")
