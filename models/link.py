import string
import random
from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class ShortenedLink(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    original_url = db.Column(db.String(2048), nullable=False)
    short_code = db.Column(db.String(10), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<ShortenedLink {self.short_code}>'

def generate_short_code(length=6):
    """Generates a random short code using letters and digits."""
    characters = string.ascii_letters + string.digits
    short_code = ''.join(random.choice(characters) for _ in range(length))
    return short_code

def create_shortened_link(original_url, custom_code=None, expiration_days=None):
    """Creates a shortened link and saves it to the database."""
    if custom_code:
        short_code = custom_code
    else:
        short_code = generate_short_code()

    # Ensure the short code is unique
    while ShortenedLink.query.filter_by(short_code=short_code).first():
        short_code = generate_short_code()

    expires_at = None
    if expiration_days:
        expires_at = datetime.utcnow() + timedelta(days=expiration_days)

    new_link = ShortenedLink(
        original_url=original_url,
        short_code=short_code,
        expires_at=expires_at
    )
    
    db.session.add(new_link)
    db.session.commit()

    return short_code

def get_original_url(short_code):
    """Retrieves the original URL based on the short code."""
    link = ShortenedLink.query.filter_by(short_code=short_code).first()
    
    if link and (not link.expires_at or link.expires_at > datetime.utcnow()):
        return link.original_url
    return None