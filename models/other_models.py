from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Click(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_code = db.Column(db.String(10), db.ForeignKey('shortened_link.short_code'), nullable=False)
    ip_address = db.Column(db.String(45), nullable=True)  # Can store IPv4 and IPv6 addresses
    user_agent = db.Column(db.String(256), nullable=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    referrer = db.Column(db.String(512), nullable=True)

    def __repr__(self):
        return f'<Click {self.short_code} - {self.timestamp}>'

class Analytics(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    short_code = db.Column(db.String(10), db.ForeignKey('shortened_link.short_code'), nullable=False)
    total_clicks = db.Column(db.Integer, default=0)
    last_clicked = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f'<Analytics {self.short_code} - {self.total_clicks} clicks>'

def log_click(short_code, ip_address=None, user_agent=None, referrer=None):
    """Logs a click event and updates analytics for a shortened link."""
    click = Click(
        short_code=short_code,
        ip_address=ip_address,
        user_agent=user_agent,
        referrer=referrer
    )
    db.session.add(click)

    # Update analytics
    analytics = Analytics.query.filter_by(short_code=short_code).first()
    if analytics:
        analytics.total_clicks += 1
        analytics.last_clicked = datetime.utcnow()
    else:
        analytics = Analytics(
            short_code=short_code,
            total_clicks=1,
            last_clicked=datetime.utcnow()
        )
        db.session.add(analytics)

    db.session.commit()

def get_clicks(short_code):
    """Retrieves the total clicks and last click time for a given short code."""
    analytics = Analytics.query.filter_by(short_code=short_code).first()
    if analytics:
        return {
            'total_clicks': analytics.total_clicks,
            'last_clicked': analytics.last_clicked
        }
    return None