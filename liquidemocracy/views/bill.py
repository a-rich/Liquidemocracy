from flask import Blueprint, request, jsonify
from flask_jwt_simple import jwt_required, get_jwt_identity
from liquidemocracy.models import User

bill = Blueprint('bill', __name__)

@bill.route('/api/bill/watch/<bill_id>/', methods=['GET'])
@jwt_required
def watch_bill(bill_id):
    """
        This endpoint adds the bill identified by the request parameter
        'bill_id' to the user's watched bills.
    """

    try:
        user = User.objects.get(email=get_jwt_identity())
    except Exception as e:
        print(e)
        return jsonify(error='Failure: no user {} in the database.'.format(get_jwt_identity()))

    #TODO: get the bill from the Bill model and add it to the user's 'watching'

    return jsonify(msg='User {} retrieved bill with ID={}'.format(get_jwt_identity(), bill_id))


@bill.route('/api/bill/comment/', methods=['POST'])
@jwt_required
def comment():
    """
        This endpoint adds a comment to the given bill's discussion object.
    """

    req = request.get_json()
    bill_id = req['bill_id']
    parent = req['parent']
    text = req['text']

    try:
        user = User.objects.get(email=get_jwt_identity())
    except Exception as e:
        print(e)
        return jsonify(error='Failure: no user {} in the database.'.format(get_jwt_identity()))

    name = user.name

    #TODO: insert comment into Bill model

    return jsonify(msg='User {} submitted comment under comment with ID={} and bill with ID={}'.format(get_jwt_identity(), parent, bill_id))


@bill.route('/api/bill/comment/upvote/', methods=['POST'])
@jwt_required
def upvote_comment():
    """
        This endpoint increments the 'upvote' attribute of the given comment of
        the given bill.
    """

    req = request.get_json()
    bill_id = req['bill_id']
    comment_id = req['comment_id']
    #TODO: update upvote count for comment of bill in the Bill model

    return jsonify(msg='User {} upvoted comment with ID={} and bill with ID={}'.format(get_jwt_identity(), comment_id, bill_id))


@bill.route('/api/bill/vote/', methods=['POST'])
@jwt_required
def vote():
    """
        This endpoint updates the votes for the bill and adds the bill to the
        vote history for the user.
    """

    req = request.get_json()
    bill_id = req['bill_id']
    vote = req['vote']

    try:
        user = User.objects.get(email=get_jwt_identity())
    except Exception as e:
        print(e)
        return jsonify(error='Failure: no user {} in the database.'.format(get_jwt_identity()))

    #TODO: update 'votes' for bill and 'voted on bills' for user

    return jsonify(msg='User {} voted \'{}\' on bill with ID={}'.format(get_jwt_identity(), vote, bill_id))

@bill.route('/api/retrieve_delegates/', methods=['GET'])
@jwt_required
def retrieve_delegates():
    """
        Returns a list of the user's delegates so that they may delegate a vote
        to one of them.
    """

    try:
        user = User.objects.get(email=get_jwt_identity())
    except Exception as e:
        print(e)
        return jsonify(error='Failure: no user {} in the database.'.format(get_jwt_identity()))

    delegates = [{d.user_id: d.name} for d in user.delegates]

    return jsonify(delegates=delegates)


@bill.route('/api/bill/delegate/', methods=['POST'])
@jwt_required
def delegate():
    """
        This endpoint gives a vote for the given bill to the given delegate.
    """

    req = request.get_json()
    bill_id = req['bill_id']
    delegate = req['delegate']

    try:
        user = User.objects.get(email=get_jwt_identity())
    except Exception as e:
        print(e)
        return jsonify(error='Failure: no user {} in the database.'.format(get_jwt_identity()))

    #TODO: get user's delegate and allocate a vote to them for the given bill

    return jsonify(msg='User {} delegated a vote for bill with ID={} to user with ID={}'.format(get_jwt_identity(), bill_id, "ObjectId('5a4d51db98bfd522c1a72e49')"))
