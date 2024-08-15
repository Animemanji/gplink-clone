from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from ad_redirect import ad_redirect_bp
from link_management import link_management_bp
from other_models import ShortenedLink, db

# Create Flask app
app = Flask(__name__)

# Configure the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///links.db'  # Use a file-based SQLite database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'  # Secret key for session management

# Initialize the database
db.init_app(app)

# Register Blueprints
app.register_blueprint(ad_redirect_bp)
app.register_blueprint(link_management_bp, url_prefix='/api')

@app.before_first_request
def create_tables():
    """Create database tables before the first request."""
    with app.app_context():
        db.create_all()

# Define a simple home route
@app.route('/')
def home():
    return 'Welcome to the URL Shortener and Ad Redirect Service!'

if __name__ == '__main__':
    app.run(debug=True)