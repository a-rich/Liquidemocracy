from flask import Blueprint, request, jsonify
from flask_jwt_simple import jwt_required, get_jwt_identity
from liquidemocracy.models import User, DelegatedVote, Bill

bill = Blueprint('bill', __name__)

@bill.route('/api/bill/watch/', methods=['GET'])
@jwt_required
def watch_bill():
    """
        This endpoint adds the bill identified by the request parameter
        'bill_id' to the user's watched bills.
    """

    req = request.get_json()
    bill_id = req['bill_id']

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
        return jsonify(error='Failure: no user {} in the database.'.format(get_jwt_identity()))

    bill = Bill.objects.get(id=bill_id)

    if bill_id in user.cast_votes \
            or bill_id in [v.bill_id for v in user.delegated_votes] \
            or bill.category in [c.category for c in user.delegated_categories]:

        return jsonify(msg='You have either cast or delegated a vote on this bill or otherwise delegated the category this bill belongs in to another user.')

    vote_weight = 0
    delegating_users = []
    for received_vote in user.received_votes:
        if bill_id == received_vote.bill_id:
            delegating_users.append(received_vote.delegator)
            vote_weight += 1
    for received_category in user.received_categories:
        if bill.category == received_category \
            and received_category.delegator not in delegating_users:
                vote_weight += 1

    if vote == 'yay':
        bill.vote_info.yay += vote_weight
    elif vote == 'nay':
        bill.vote_info.nay += vote_weight

    user.cast_votes.append(bill_id)

    user.save()

    return jsonify(msg='User {} voted \'{}\' on bill with ID={} with a vote weight {}'.format(
        get_jwt_identity(), vote, bill_id, vote_weight))


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

    return jsonify(delegates)


@bill.route('/api/bill/delegate/', methods=['POST'])
@jwt_required
def delegate():
    """
        This endpoint gives a vote for the given bill to the given delegate.
    """

    req = request.get_json()
    bill_id = req['bill_id']
    delegate_id = req['delegate']

    try:
        user = User.objects.get(email=get_jwt_identity())
    except Exception as e:
        return jsonify(msg='Failure: no user {} in the database.'.format(get_jwt_identity()))

    try:
        delegate = User.objects.get(id=delegate_id)
    except Exception as e:
        return jsonify(msg='Failure: no user {} in the database.'.format(delegate_id))

    delegated_vote = DelegatedVote(
            delegator=user.id,
            delegate=delegate_id,
            bill_id=bill_id)

    user.delegated_votes.append(delegated_vote)
    delegate.received_votes.append(delegated_vote)

    user.save()
    delegate.save()

    return jsonify(msg='success')
