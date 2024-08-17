import unittest
from app import create_app, db
from app.models import Ad

class AdRedirectTestCase(unittest.TestCase):

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

    def test_ad_redirect(self):
        # Create a test ad entry
        ad = Ad(url='https://example.com/ad')
        db.session.add(ad)
        db.session.commit()

        # Test the ad redirect
        response = self.client.get(f'/ad/{ad.id}')
        self.assertEqual(response.status_code, 302)
        self.assertIn('example.com', response.headers['Location'])

if __name__ == '__main__':
    unittest.main()