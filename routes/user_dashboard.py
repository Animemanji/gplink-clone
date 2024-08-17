from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Link
from . import db

user_dashboard = Blueprint('user_dashboard', __name__)

@user_dashboard.route('/dashboard')
@login_required
def dashboard():
    # Fetch all links created by the logged-in user
    user_links = Link.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', links=user_links)

@user_dashboard.route('/delete-link/<int:link_id>')
@login_required
def delete_link(link_id):
    # Find the link by ID and ensure it belongs to the current user
    link_to_delete = Link.query.get_or_404(link_id)
    if link_to_delete.user_id != current_user.id:
        flash('Unauthorized action', 'danger')
        return redirect(url_for('user_dashboard.dashboard'))
    
    # Delete the link and commit the change to the database
    db.session.delete(link_to_delete)
    db.session.commit()
    flash('Link deleted successfully', 'success')
    return redirect(url_for('user_dashboard.dashboard'))