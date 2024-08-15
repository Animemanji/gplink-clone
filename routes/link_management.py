from flask import Blueprint, request, jsonify, abort
from link import create_shortened_link, get_original_url
from other_models import ShortenedLink, db

link_management_bp = Blueprint('link_management', __name__)

@link_management_bp.route('/create_link', methods=['POST'])
def create_link():
    """Creates a new shortened link."""
    data = request.json
    original_url = data.get('original_url')
    custom_code = data.get('custom_code', None)
    expiration_days = data.get('expiration_days', None)

    if not original_url:
        return jsonify({'error': 'Original URL is required'}), 400

    try:
        expiration_days = int(expiration_days) if expiration_days else None
    except ValueError:
        return jsonify({'error': 'Invalid expiration days'}), 400

    short_code = create_shortened_link(original_url, custom_code, expiration_days)
    short_link = request.host_url + short_code
    return jsonify({'short_link': short_link}), 201

@link_management_bp.route('/update_link/<short_code>', methods=['PUT'])
def update_link(short_code):
    """Updates the expiration of an existing shortened link."""
    data = request.json
    new_expiration_days = data.get('new_expiration_days')

    try:
        new_expiration_days = int(new_expiration_days) if new_expiration_days else None
    except ValueError:
        return jsonify({'error': 'Invalid expiration days'}), 400

    link = ShortenedLink.query.filter_by(short_code=short_code).first()
    if link:
        if new_expiration_days:
            link.expires_at = datetime.utcnow() + timedelta(days=new_expiration_days)
        else:
            link.expires_at = None
        db.session.commit()
        return jsonify({'message': 'Link updated successfully'}), 200
    else:
        return jsonify({'error': 'Short code not found'}), 404

@link_management_bp.route('/delete_link/<short_code>', methods=['DELETE'])
def delete_link(short_code):
    """Deletes a shortened link."""
    link = ShortenedLink.query.filter_by(short_code=short_code).first()
    if link:
        db.session.delete(link)
        db.session.commit()
        return jsonify({'message': 'Link deleted successfully'}), 200
    else:
        return jsonify({'error': 'Short code not found'}), 404