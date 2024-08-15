import unittest
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from link_management import link_management_bp
from datetime import datetime, timedelta

# Setup Flask application and database for testing
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['TESTING'] = True
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)

# Register Blueprint
app.register_blueprint(link_management_bp, url_prefix='/api')

# Define ShortenedLink model for testing
class ShortenedLink(db.Model):
    short_code = db.Column(db.String(10), primary_key=True)
    original_url = db.Column(db.String(512), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=True)

# Create test database
with app.app_context():
    db.create_all()

class LinkManagementTests(unittest.TestCase):
    def setUp(self):
        """Set up test client and initialize test data."""
        self.client = app.test_client()
        self.client.testing = True

    def tearDown(self):
        """Clean up after each test."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_create_link(self):
        """Test creating a new shortened link."""
        response = self.client.post('/api/create_link', json={
            'original_url': 'https://example.com',
            'custom_code': 'testcode',
            'expiration_days': 30
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('short_link', response.json)
        self.assertTrue(response.json['short_link'].startswith(request.host_url))

    def test_update_link(self):
        """Test updating the expiration of an existing link."""
        # First, create a link
        self.client.post('/api/create_link', json={
            'original_url': 'https://example.com',
            'custom_code': 'testcode',
            'expiration_days': 30
        })

        # Now, update the link
        response = self.client.put('/api/update_link/testcode', json={
            'new_expiration_days': 60
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Link updated successfully')

        # Check the updated expiration date
        link = ShortenedLink.query.filter_by(short_code='testcode').first()
        self.assertIsNotNone(link.expires_at)
        self.assertTrue(link.expires_at > datetime.utcnow() + timedelta(days=29))

    def test_delete_link(self):
        """Test deleting an existing link."""
        # First, create a link
        self.client.post('/api/create_link', json={
            'original_url': 'https://example.com',
            'custom_code': 'testcode',
            'expiration_days': 30
        })

        # Now, delete the link
        response = self.client.delete('/api/delete_link/testcode')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json['message'], 'Link deleted successfully')

        # Ensure the link has been deleted
        link = ShortenedLink.query.filter_by(short_code='testcode').first()
        self.assertIsNone(link)

if __name__ == '__main__':
    unittest.main()