
import unittest
import json
from app import app, get_db, ENCRYPTION_KEY
from cryptography.fernet import Fernet

class TestApp(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.db = get_db()
        
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
        self.assertIn('message', data)

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
        self.assertIn('message', data)

    def test_get_users(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)

def test_wrong_encryption_key(self):
        # Create an event with the correct key
        response = self.app.post('/events', json={
            'name': 'Secret Event',
            'date': '2023-05-01 10:00:00',
            'description': 'This is a secret event'
        })
        self.assertEqual(response.status_code, 201)

        # Try to access events with a wrong key
        wrong_key = Fernet.generate_key()
        with self.assertRaises(ValueError):
            get_db(wrong_key)

        # Verify that we can still access events with the correct key
        response = self.app.get('/events')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertIsInstance(data, list)
        self.assertTrue(any(event['name'] == 'Secret Event' for event in data))

if __name__ == '__main__':
    unittest.main()
