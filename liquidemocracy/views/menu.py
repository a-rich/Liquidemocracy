from flask import Blueprint, jsonify
from flask_jwt_simple import jwt_required, get_jwt_identity
from liquidemocracy.models import User

menu = Blueprint('menu', __name__)

@menu.route('/api/profile/', methods=['GET'])
@jwt_required
def profile():
    """
        This endpoint returns the user's name, email, and residence (city,
        county, state).
    """

    try:
        user = User.objects.get(email=get_jwt_identity())
    except Exception as e:
        print(e)
        return jsonify(error=str(e))

    res = {
        'name': user.name,
        'email': user.email,
        'residence': {
            'city': user.city,
            'county': user.county,
            'state': user.state,
        }
    }

    return jsonify(res=res)


@menu.route('/api/votes/active/', methods=['GET'])
def active_votes():
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
