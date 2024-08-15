from flask import Blueprint, render_template, redirect, url_for, session, request
from datetime import datetime, timedelta

ad_redirect_bp = Blueprint('ad_redirect', __name__)

@ad_redirect_bp.route('/ad/<short_code>')
def show_ad(short_code):
    """Renders the ad page and stores the timestamp of the visit."""
    session['ad_view_time'] = datetime.utcnow()
    session['short_code'] = short_code
    return render_template('ad_page.html')

@ad_redirect_bp.route('/redirect')
def redirect_after_ad():
    """Redirects the user to the original URL after the ad has been shown for 10 seconds."""
    ad_view_time = session.get('ad_view_time')
    short_code = session.get('short_code')

    if not ad_view_time or not short_code:
        return 'Ad viewing session expired or not found', 400

    # Ensure the user has viewed the ad for at least 10 seconds
    if datetime.utcnow() - ad_view_time >= timedelta(seconds=10):
        # Redirect to the final destination page
        return redirect(url_for('link.redirect_to_original_url', short_code=short_code))
    else:
        remaining_time = 10 - (datetime.utcnow() - ad_view_time).seconds
        return f'Please wait {remaining_time} more seconds.', 403