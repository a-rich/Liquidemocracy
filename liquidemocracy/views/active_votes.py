from flask import Blueprint, request, jsonify
from flask_jwt_simple import jwt_required, get_jwt_identity
from flask import current_app as app
from liquidemocracy.models import User

active_votes = Blueprint('active_votes', __name__)

@active_votes.route('/api/delegates/search/<query>/', methods=['GET'])
@jwt_required
def search_delegates(query):
    """
        This endpoint queries the User model for all space delimited substrings
        of the query.
    """

    results = [
        {
            'user_id': "ObjectId('5a4d51db98bfd522c1a72e49')",
            'name': 'Alex Richards'
        },
        {
            'user_id': "ObjectId('5a4e6cab98bfd51b98a47219')",
            'name': 'Alex Trebek'
        }
    ]

    return jsonify(results=results)


@active_votes.route('/api/delegate/', methods=['POST'])
@jwt_required
def delegate():
    """
        This endpoint accepts a delegation type of either 'bill' or 'category',
        the ID of the bill or category, and the ID of the user who will receive
        this delegation.
    """

    req = request.get_json()
    delegation_type = req['type']
    delegation_id = req['delegation_id']
    user_id = req['user_id']

    return jsonify(msg='Delegating {} with ID={} to {}'.format(delegation_type, delegation_id, user_id))
