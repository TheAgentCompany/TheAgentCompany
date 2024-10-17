
import unittest
import json
from app import app, get_db, DB_PASSWORD

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.db = get_db()
        self.db.execute(f"PRAGMA key='{DB_PASSWORD}'")
        
    def tearDown(self):
        self.db.close()

    def test_create_event(self):
        response = self.app.post('/events', json={
            'name': 'Test Event',
            'date': '2023-05-01 10:00:00',
            'description': 'This is a test event'
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)

    def test_get_events(self):
        response = self.app.get('/events')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_create_user(self):
        response = self.app.post('/users', json={
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)

    def test_get_users(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

    def test_create_participant(self):
        # First, create a user and an event
        user_response = self.app.post('/users', json={
            'username': 'testuser2',
            'email': 'testuser2@example.com',
            'password': 'testpassword'
        })
        user_data = json.loads(user_response.data)
        
        event_response = self.app.post('/events', json={
            'name': 'Test Event 2',
            'date': '2023-05-02 11:00:00',
            'description': 'This is another test event'
        })
        event_data = json.loads(event_response.data)
        
        # Now create a participant
        response = self.app.post('/participants', json={
            'user_id': user_data['id'],
            'event_id': event_data['id']
        })
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertIn('id', data)

    def test_get_participants(self):
        response = self.app.get('/participants')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

if __name__ == '__main__':
    unittest.main()
