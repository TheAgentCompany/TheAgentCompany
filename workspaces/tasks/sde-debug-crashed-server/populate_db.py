import os
import pyarrow as pa
import pyarrow.parquet as pq
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
import base64
from faker import Faker
import random
from datetime import datetime, timedelta

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

fake = Faker()

def generate_fake_data():
    # Generate users
    users = [
        (i, fake.name(), fake.email())
        for i in range(1, 51)  # 50 users
    ]

    # Generate events
    events = [
        (i, fake.catch_phrase(), fake.date_between(start_date='-1y', end_date='+1y').isoformat())
        for i in range(1, 31)  # 30 events
    ]

    # Generate participants
    participants = [
        (i, random.randint(1, 50), random.randint(1, 30))
        for i in range(1, 101)  # 100 participants
    ]

    return users, events, participants

def encrypt_and_save_data(data, file_name):
    # Convert tuples to dictionaries
    if file_name == 'users':
        dict_data = [{'id': u[0], 'name': u[1], 'email': u[2]} for u in data]
    elif file_name == 'events':
        dict_data = [{'id': e[0], 'description': e[1], 'date': e[2]} for e in data]
    elif file_name == 'participants':
        dict_data = [{'id': p[0], 'user_id': p[1], 'event_id': p[2]} for p in data]
    else:
        raise ValueError(f"Unknown file_name: {file_name}")

    table = pa.Table.from_pylist(dict_data)
    buffer = pa.BufferOutputStream()
    pq.write_table(table, buffer)
    encrypted_data = fernet.encrypt(buffer.getvalue().to_pybytes())
    
    # Get the parent directory of the current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)
    
    # Create the database directory if it doesn't exist
    db_dir = os.path.join(parent_dir, 'database')
    os.makedirs(db_dir, exist_ok=True)
    
    # Save the file in the database directory
    file_path = os.path.join(db_dir, f'{file_name}.parquet')
    with open(file_path, 'wb') as f:
        f.write(encrypted_data)

if __name__ == "__main__":
    users, events, participants = generate_fake_data()
    
    encrypt_and_save_data(users, 'users')
    encrypt_and_save_data(events, 'events')
    encrypt_and_save_data(participants, 'participants')
    
    print("Fake data has been generated and saved to encrypted parquet files.")
