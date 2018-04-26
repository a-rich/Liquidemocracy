from flask import Blueprint, request, jsonify
from flask_jwt_simple import jwt_required, get_jwt_identity
from flask import current_app as app
from liquidemocracy.models import *

active_votes = Blueprint('active_votes', __name__)

@active_votes.route('/api/delegate/search/', methods=['POST'])
@jwt_required
def search_delegate():
    """
        This endpoint queries the User model for all space delimited substrings
        of the query.
    """

    user = User.objects(email=request.get_json()['query']).only('id', 'name')

    return jsonify(user)

@active_votes.route('/api/delegate/add/', methods=['POST'])
@jwt_required
def add_delegate():
    """
    """

    req = request.get_json()
    user = User.objects.get(email=get_jwt_identity())
    delegate = User.objects.get(id=req['delegate_id'])
    delegate_obj = Delegate(user_id=delegate.id, name=delegate.name)
    user.delegates.append(delegate_obj)

    return jsonify(msg="Successfully added {} to {}'s delegates list".format(
            delegate.name, user.name))

@active_votes.route('/api/delegate/', methods=['POST'])
@jwt_required
def delegate():
    """
    """

    req = request.get_json()

    return jsonify()


@active_votes.route('/api/votes/active/', methods=['GET'])
@jwt_required
def votes_active():
    """
        This endpoint returns the data for the active votes view. This includes
        'delegations' (just 'people' -- note: 'legislation' is the same data as
        is in 'people' so it is not sent twice...the client-side must map
        'people' date to 'legislation' data), 'representative_for', 'my_votes',
        and 'watching'.
    """

    res = {
        'delegations': {
            'people': {
                "ObjectId('5a4d51db98bfd522c1a72e49')": {
                    'name': 'Alex Richards',
                    'bills': [
                        {
                            'bill_id': 0,
                            'title': 'some bill',
                            'vote_date': '2018-06-01 12:00:00',
                            'level': 'city',
                            'vote': 'yes'
                        },
                        {
                            'bill_id': 1,
                            'title': 'another bill',
                            'vote_date': '2018-07-04 12:00:00',
                            'level': 'state',
                            'vote': 'None'
                        }
                    ],
                    'categories': [
                        {
                            'category_id': 0,
                            'title': 'Technology',
                            'level': 'state',
                            'vote_count': '7/34'
                        },
                        {
                            'category_id': 1,
                            'title': 'Education',
                            'level': 'state',
                            'vote_count': '13/27'
                        }
                    ]
                }
            }
        },
        'representative_for': {
            'bills': [
                {
                    'bill_id': 0,
                    'title': 'some bill',
                    'vote_date': '2018-06-01 12:00:00',
                    'level': 'city',
                    'vote': 'yes',
                    'constituent_count': '2'
                },
                {
                    'bill_id': 1,
                    'title': 'another bill',
                    'vote_date': '2018-07-04 12:00:00',
                    'level': 'state',
                    'vote': 'None',
                    'constituent_count': '1'
                }
            ],
            'categories': [
                {
                    'category_id': 0,
                    'title': 'Technology',
                    'level': 'state',
                    'vote_count': '7/34',
                    'constituent_count': '1'
                },
                {
                    'category_id': 1,
                    'title': 'Education',
                    'level': 'state',
                    'vote_count': '13/27',
                    'constituent_count': '4'
                }
            ]
        },
        'my_votes': [
            {
                'bill_id': 0,
                'title': 'some bill',
                'vote_date': '2018-06-01 12:00:00',
                'level': 'city',
                'vote': 'yes',
            },
            {
                'bill_id': 1,
                'title': 'another bill',
                'vote_date': '2018-07-04 12:00:00',
                'level': 'state',
                'vote': 'None',
            }
        ],
        'watching': [
            {
                'bill_id': 0,
                'title': 'some bill',
                'vote_date': '2018-06-01 12:00:00',
                'level': 'city',
                'vote': 'yes',
            },
            {
                'bill_id': 1,
                'title': 'another bill',
                'vote_date': '2018-07-04 12:00:00',
                'level': 'state',
                'vote': 'None',
            }
        ]
    }

    return jsonify(res=res)
