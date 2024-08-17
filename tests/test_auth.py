import unittest
from flask import Flask
from flask_login import current_user
from app import create_app, db
from app.models import User

class AuthTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_signup(self):
        response = self.client.post('/signup', data={
            'email': 'test@example.com',
            'username': 'testuser',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after signup
        user = User.query.filter_by(email='test@example.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.username, 'testuser')

    def test_login(self):
        user = User(email='login@example.com', username='loginuser', password='hashed_password')
        db.session.add(user)
        db.session.commit()
        response = self.client.post('/login', data={
            'email': 'login@example.com',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(current_user.is_authenticated)

    def test_logout(self):
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 302)
        self.assertFalse(current_user.is_authenticated)

if __name__ == '__main__':
    unittest.main()