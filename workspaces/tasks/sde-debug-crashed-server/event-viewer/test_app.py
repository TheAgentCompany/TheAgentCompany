import os
import unittest
import json
from app import app, db, User, Event, Participant

os.environ['DB_PASSWORD'] = 'test_password'

class TestApp(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        self.client = app.test_client()

        with app.app_context():
            db.create_all()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_user(self):
        response = self.client.post('/user', json={'username': 'testuser', 'password': 'testpass'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('User created successfully', response.get_json()['message'])

    def test_get_user(self):
        self.client.post('/user', json={'username': 'testuser', 'password': 'testpass'})
        response = self.client.get('/user/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['username'], 'testuser')

    def test_create_event(self):
        response = self.client.post('/event', json={'name': 'Test Event', 'description': 'This is a test event'})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Event created successfully', response.get_json()['message'])

    def test_get_event(self):
        self.client.post('/event', json={'name': 'Test Event', 'description': 'This is a test event'})
        response = self.client.get('/event/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['name'], 'Test Event')

    def test_create_participant(self):
        self.client.post('/user', json={'username': 'testuser', 'password': 'testpass'})
        self.client.post('/event', json={'name': 'Test Event', 'description': 'This is a test event'})
        response = self.client.post('/participant', json={'user_id': 1, 'event_id': 1})
        self.assertEqual(response.status_code, 201)
        self.assertIn('Participant added successfully', response.get_json()['message'])

    def test_get_events_list(self):
        # Create a test event
        self.client.post('/event', json={'name': 'Test Event 1', 'description': 'This is test event 1'})
        self.client.post('/event', json={'name': 'Test Event 2', 'description': 'This is test event 2'})
        
        response = self.client.get('/events')
        self.assertEqual(response.status_code, 200)
        events = response.get_json()
        self.assertIsInstance(events, list)
        self.assertGreater(len(events), 0)
        self.assertEqual(len(events), 2)

    def test_get_users_list(self):
        # Create test users
        self.client.post('/user', json={'username': 'testuser1', 'password': 'testpass1'})
        self.client.post('/user', json={'username': 'testuser2', 'password': 'testpass2'})
        
        response = self.client.get('/users')
        self.assertEqual(response.status_code, 200)
        users = response.get_json()
        self.assertIsInstance(users, list)
        self.assertGreater(len(users), 0)
        self.assertEqual(len(users), 2)

    def test_get_participants_list(self):
        # Create test users and events
        self.client.post('/user', json={'username': 'testuser1', 'password': 'testpass1'})
        self.client.post('/user', json={'username': 'testuser2', 'password': 'testpass2'})
        self.client.post('/event', json={'name': 'Test Event', 'description': 'This is a test event'})
        
        # Add participants
        self.client.post('/participant', json={'user_id': 1, 'event_id': 1})
        self.client.post('/participant', json={'user_id': 2, 'event_id': 1})
        
        response = self.client.get('/participants')
        self.assertEqual(response.status_code, 200)
        participants = response.get_json()
        self.assertIsInstance(participants, list)
        self.assertGreater(len(participants), 0)
        self.assertEqual(len(participants), 2)

def test_wrong_password(self):
        from contextlib import contextmanager

        @contextmanager
        def temp_env_var(key, value):
            original_value = os.environ.get(key)
            os.environ[key] = value
            try:
                yield
            finally:
                if original_value is None:
                    del os.environ[key]
                else:
                    os.environ[key] = original_value

        with temp_env_var('DB_PASSWORD', 'wrong_password'):
            with self.assertRaises(ValueError):
                from app import verify_db_password
                verify_db_password()

if __name__ == '__main__':
    unittest.main()
