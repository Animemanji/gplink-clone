import unittest
from flask import Flask, session
from flask_sqlalchemy import SQLAlchemy
from ad_redirect import ad_redirect_bp
from link_management import link_management_bp
from datetime import datetime, timedelta
import time

# Setup Flask application and database for testing
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['TESTING'] = True
app.secret_key = 'your_secret_key'
db = SQLAlchemy(app)

# Register Blueprints
app.register_blueprint(ad_redirect_bp)
app.register_blueprint(link_management_bp, url_prefix='/api')

# Define ShortenedLink model for testing
class ShortenedLink(db.Model):
    short_code = db.Column(db.String(10), primary_key=True)
    original_url = db.Column(db.String(512), nullable=False)
    expires_at = db.Column(db.DateTime, nullable=True)

# Create test database
with app.app_context():
    db.create_all()

class RedirectTests(unittest.TestCase):
    def setUp(self):
        """Set up test client and initialize test data."""
        self.client = app.test_client()
        self.client.testing = True

        # Create a test link
        self.client.post('/api/create_link', json={
            'original_url': 'https://final-destination.com',
            'custom_code': 'testcode',
            'expiration_days': 30
        })

    def tearDown(self):
        """Clean up after each test."""
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_redirect_after_ad(self):
        """Test that users are redirected after the ad page."""
        # Simulate visiting the ad page
        response = self.client.get('/ad/testcode')
        self.assertEqual(response.status_code, 200)

        # Simulate waiting for 10 seconds to ensure the ad is shown
        time.sleep(10)

        # Test redirection after waiting
        response = self.client.get('/redirect')
        self.assertEqual(response.status_code, 302)
        self.assertIn('https://final-destination.com', response.headers['Location'])

    def test_redirect_before_ad_timeout(self):
        """Test that users are blocked from redirecting before the ad timeout."""
        # Simulate visiting the ad page
        response = self.client.get('/ad/testcode')
        self.assertEqual(response.status_code, 200)

        # Simulate waiting for 5 seconds (less than the required 10 seconds)
        time.sleep(5)

        # Test that users are blocked from redirecting
        response = self.client.get('/redirect')
        self.assertEqual(response.status_code, 403)
        self.assertIn('Please wait', response.data.decode())

if __name__ == '__main__':
    unittest.main()