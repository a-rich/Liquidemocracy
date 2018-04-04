from flask import Blueprint, request, jsonify
from flask_jwt_simple import jwt_required, create_jwt, get_jwt_identity
from liquidemocracy.models import User

bill_list = Blueprint('bill_list', __name__)

@bill_list.route('/api/login/', methods=['POST'])
def login():
    """
        This endpoint finds a user in the User model with the same
        email/password, creates a JWT, and returns it. If the provided
        credentials did not return a user from the User model, the returned
        JSON object will instead include an error string stating this.
    """

    #TODO: log error

    req = request.get_json()
    email = req['email']
    password = req['password']

    try:
        user = User.objects.get(email=req['email'], password=req['password'])
        token = create_jwt(identity=email)
        return jsonify(jwt=token)
    except Exception as e:
        print(e)
        return jsonify(error='Invalid credentials. Please try again.')


@bill_list.route('/api/bills/', methods=['POST'])
@jwt_required
def bills():
    """
        This endpoint queries the Bill model for bills matching the provided
        'level', filtered using the provided 'filter', and returns them in a
        list sorted by the order specified in the 'sort' attribute.
    """

    req = request.get_json()
    level = req['options']['level']
    bill_filter = req['options']['filter']
    sort = req['options']['sort']

    if level is not 'federal' or bill_filter is not 'all' \
            or sort is 'recommended':
        try:
            user = User.objects.get(email=get_jwt_identity())
        except Exception as e:
            print(e)

    #TODO: log error
    #TODO: replace hard coded bills with a query to the Bill model
    bills = [
        {0: {
            'title': 'some bill',
            'vote_date': '2018-06-01 12:00:00',
            'level': 'city'
            }},
        {1: {
            'title': 'another bill',
            'vote_date': '2018-07-04 12:00:00',
            'level': 'state'
            }}
    ]

    return jsonify(bills=bills)


@bill_list.route('/api/bills/default/', methods=['POST'])
def default_bills():
    """
        This endpoint queries the Bill model for all federal bills and returns
        their 'title' and 'vote_date' in a list sorted by the order specified
        in the 'sort' attribute.
    """

    req = request.get_json()
    sort = req['options']['sort']

    #TODO: replace hard coded bills with a query to the Bill model
    bills = [
        {0: {'title': 'some bill', 'vote_date': '2018-06-01 12:00:00'}},
        {1: {'title': 'another bill', 'vote_date': '2018-07-04 12:00:00'}}
    ]

    return jsonify(bills=bills)


@bill_list.route('/api/bills/search/', methods=['POST'])
def search():
    """
        This endpoint queries the Bill model for bills having a title or
        keywords containing any space-separated substring of the query and
        returns a list of these bills.
    """

    query = request.get_json()['query']

    #TODO: replace hard coded bills with a query to the Bill model
    bills = [
        {0: {
            'title': 'some bill',
            'vote_date': '2018-06-01 12:00:00',
            'level': 'city'
            }},
        {1: {
            'title': 'another bill',
            'vote_date': '2018-07-04 12:00:00',
            'level': 'state'
            }}
    ]

    return jsonify(bills=bills)


@bill_list.route('/api/bills/<bill_id>/', methods=['GET'])
def view_bill(bill_id):
    """
        This endpoint returns the Bill matching the request parameter
        'bill_id'.
    """

    #TODO: replace hard coded bill with a query to the Bill model
    bill = {
        'title': 'some bill',
        'categories': ['technology', 'education'],
        'keywords': ['generic', 'stuff'],
        'description': "This is just a generic bill used as dummy data.",
        'vote_info': {
            'vote_date': '2018-06-01 12:00:00',
            'yay': '17',
            'nay': '12',
            'voter_count': '53'
        },
        'discussion': {
            0: {
                'date': '2018-01-03 12:36:35.822487',
                'vote_count': '4',
                'text': 'This is bill is pointless.',
                'children': {
                    2: {
                        'date': '2018-01-03 2:12:52.986234',
                        'vote_count': '2',
                        'text': 'I concur.',
                        'children': {}
                    }
                }
            },
            1: {
                'date': '2018-01-03 12:38:15.28763',
                'vote_count': '0',
                'text': 'I love this bill. We need more just like it.',
                'children': {
                    3: {
                        'date': '2018-01-03 12:43:27.396273',
                        'vote_count': '9',
                        'text': 'You are the reason our country is going down the drain.',
                        'children': {}
                    }
                }
            }
        }
    }

    return jsonify(bill=bill)
