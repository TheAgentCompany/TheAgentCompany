import os
import unittest
import tempfile
import sqlite3
from app import app

class TestApp(unittest.TestCase):
    def setUp(self):
        self.db_fd, self.db_path = tempfile.mkstemp()
        app.config['DATABASE'] = self.db_path
        app.config['TESTING'] = True
        self.client = app.test_client()

        # Create and populate test database
        self.db = sqlite3.connect(self.db_path)
        self.db.execute("PRAGMA key='cat123'")
        self.db.execute('''
            CREATE TABLE events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT
            )
        ''')
        self.db.execute("INSERT INTO events (name, date, description) VALUES (?, ?, ?)",
                       ('Test Event', '2024-01-01', 'Test Description'))
        self.db.commit()
        self.db.close()

    def tearDown(self):
        os.close(self.db_fd)
        os.unlink(self.db_path)

    def test_correct_password(self):
        """Test that the API works with the correct password."""
        os.environ['DB_PASSWORD'] = 'cat123'
        response = self.client.get('/events')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertTrue(len(data) > 0)
        self.assertEqual(data[0]['name'], 'Test Event')

    def test_incorrect_password(self):
        """Test that the API fails with an incorrect password."""
        os.environ['DB_PASSWORD'] = 'wrong_password'
        response = self.client.get('/events')
        self.assertEqual(response.status_code, 500)  # Should fail to access database

    def test_no_password(self):
        """Test that the API fails with no password."""
        if 'DB_PASSWORD' in os.environ:
            del os.environ['DB_PASSWORD']
        response = self.client.get('/events')
        self.assertEqual(response.status_code, 500)  # Should fail to access database

if __name__ == '__main__':
    unittest.main()