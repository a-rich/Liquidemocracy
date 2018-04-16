from flask import Blueprint, request, jsonify
from flask_jwt_simple import jwt_required, create_jwt, get_jwt_identity
from liquidemocracy.models import User, Bill
import liquidemocracy.bill_recommender.recommender as recommender

bill_list = Blueprint('bill_list', __name__)

all_levels = [
        'federal',
        'states',
        'counties',
        'cities'
        ]

all_categories = [
            'Taxation',
            'Health',
            'Armed Forces and National Security',
            'Foreign Trade and International Finance',
            'International Affairs',
            'Crime and Law Enforcement',
            'Transportation and Public Works',
            'Education',
            'Energy',
            'Agriculture and Food',
            'Economics and Public Finance',
            'Labor and Employment',
            'Environmental Protection',
            'Science, Technology, Communications',
            'Immigration',
            'Other'
            ]

limit = 100

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


@bill_list.route('/api/bills/default/', methods=['POST'])
def default_bills():
    """
        This endpoint queries the Bill model for all federal bills and returns
        their 'title' and 'vote_date' in a list sorted by the order specified
        in the 'sort' attribute.
    """

    req = request.get_json()
    query = req['query']
    category = req['category']
    index = req['index'] * limit

    categories = [category] if category else all_categories

    if query:
        bills = Bill.objects(
                title__icontains=query,
                level='federal',
                category__in=categories).order_by('-date').only(
                'id', 'title', 'category', 'level', 'date')[index:index+limit]
    else:
        bills = Bill.objects(
                level='federal',
                category__in=categories).order_by('-date').only(
                'id', 'title', 'category', 'level', 'date')[index:index+limit]

    return jsonify(bills=bills)


@bill_list.route('/api/bills/', methods=['POST'])
@jwt_required
def bills():
    """
        This endpoint queries the Bill model for bills matching the provided
        'level', filtered using the provided 'filter', and returns them in a
        list sorted by the order specified in the 'sort' attribute.
    """

    req = request.get_json()
    query = req['query']
    level = req['level']
    bill_filter = req['filter']
    category = req['category']
    index = req['index'] * limit

    try:
        email=get_jwt_identity()
    except Exception as e:
        print(e)
        return jsonify(error='Invalid credentials. Try loging in again.')

    levels= [level] if level else all_levels
    categories = [category] if category else all_categories

    if bill_filter == 'recommended':
        bills = recommender.recommend_bills(email, levels, index, limit, query)
    elif query:
        bills = Bill.objects(
                title__icontains=query,
                level__in=levels,
                category__in=categories).order_by('-date').only(
                    'id', 'title', 'category', 'level', 'date')[index:index+limit]
    else:

        categories = ['Environmental Protection', 'Energy', 'Science, Technology, Communications']

        bills = Bill.objects(
                level__in=levels,
                category__in=categories).order_by('-date').only(
                    'id','title', 'category', 'level', 'date')[index:index+limit]

    return jsonify(bills=bills)


@bill_list.route('/api/bills/<bill_id>/', methods=['GET'])
def view_bill(bill_id):
    """
        This endpoint returns the Bill matching the request parameter
        'bill_id'.
    """

    bill = Bill.objects(id=bill_id)

    return jsonify(bill=bill)
