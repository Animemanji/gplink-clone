from flask import Blueprint, render_template, redirect, url_for
    from .models import Ad
    from . import db
    
    ad = Blueprint('ad', __name__)
    
    @ad.route('/ad/<int:ad_id>')
    def show_ad(ad_id):
        # Fetch the ad by ID
        advertisement = Ad.query.get_or_404(ad_id)
    
        # Here, you might want to track that the ad was viewed
        advertisement.views += 1
        db.session.commit()
    
        # Render the ad page
        return render_template('ad_page.html', ad=advertisement)
    
    @ad.route('/redirect/<int:ad_id>')
    def redirect_to_target(ad_id):
        # Fetch the ad by ID
        advertisement = Ad.query.get_or_404(ad_id)
    
        # Track the click
        advertisement.clicks += 1
        db.session.commit()
    
        # Redirect the user to the target URL
        return redirect(advertisement.target_url)