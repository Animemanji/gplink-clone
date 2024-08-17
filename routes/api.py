from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from .models import Link
from . import db
import random
import string

api = Blueprint('api', __name__)

def generate_short_code(length=6):
    """Generate a random short code."""
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

@api.route('/create-link', methods=['POST'])
@login_required
def create_link():
    data = request.get_json()
    original_url = data.get('original_url')
    custom_alias = data.get('custom_alias', '')

    # If no custom alias provided, generate a short code
    short_code = custom_alias if custom_alias else generate_short_code()

    # Check if the alias or short code is already taken
    existing_link = Link.query.filter_by(short_code=short_code).first()
    if existing_link:
        return jsonify({'error': 'This alias is already taken. Please choose another.'}), 400

    # Create a new link
    new_link = Link(
        original_url=original_url,
        short_code=short_code,
        user_id=current_user.id
    )
    db.session.add(new_link)
    db.session.commit()

    return jsonify({'short_url': f"/{short_code}"}), 201

@api.route('/links/<int:link_id>', methods=['GET'])
@login_required
def get_link(link_id):
    link = Link.query.get_or_404(link_id)
    if link.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized access'}), 403

    return jsonify({
        'original_url': link.original_url,
        'short_code': link.short_code,
        'created_at': link.created_at
    })

@api.route('/links/<int:link_id>', methods=['DELETE'])
@login_required
def delete_link_api(link_id):
    link_to_delete = Link.query.get_or_404(link_id)
    if link_to_delete.user_id != current_user.id:
        return jsonify({'error': 'Unauthorized action'}), 403

    db.session.delete(link_to_delete)
    db.session.commit()
    return jsonify({'message': 'Link deleted successfully'}), 200