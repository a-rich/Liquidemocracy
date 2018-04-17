from flask import Blueprint, request, jsonify
from flask_jwt_simple import jwt_required, get_jwt_identity
from liquidemocracy.models import *

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

    user = User.objects.get(email=get_jwt_identity())
    bill = Bill.objects.get(id=bill_id)

    def calc_vote_weight(vote):
        vote_weight = 1
        delegating_users = []
        for received_vote in user.received_votes:
            if bill.id == received_vote.cast_vote.bill_id:
                received_vote.cast_vote.vote = vote
                delegating_users.append(received_vote.delegator)
                vote_weight += 1
        for received_category in user.received_categories:
            if bill.category == received_category \
                and received_category.delegator not in delegating_users:
                    vote_weight += 1

        return vote_weight

    def cast_vote(vote_weight, vote_type='new', vote_obj=None):
        if vote_type == 'new':
            if vote == 'yay':
                bill.vote_info.yay += vote_weight
            elif vote == 'nay':
                bill.vote_info.nay += vote_weight
            new_vote = CastVote(bill_id=bill.id, vote=vote)
            user.cast_votes.append(new_vote)
        elif vote_type == 'change':
            if vote == 'yay':
                bill.vote_info.nay -= vote_weight
                bill.vote_info.yay += vote_weight
            elif vote == 'nay':
                bill.vote_info.yay -= vote_weight
                bill.vote_info.nay += vote_weight
            vote_obj.vote = vote

        bill.save()

        reformatted = '_'.join([word.lower() for word in bill.category.split()])
        vector_dict = user.interest_vector.to_mongo()
        vector_dict[reformatted] += 3
        user.interest_vector = InterestVector(**vector_dict.to_dict())

        user.save()

    for v in user.cast_votes:
        if bill.id == v.bill_id:
            if v.vote == vote:
                return jsonify(msg='You have already cast a vote on this bill.')
            else:
                vote_weight = calc_vote_weight(vote)
                cast_vote(vote_weight, vote_type='change', vote_obj=v)
                return jsonify(msg='You changed your vote on this bill.')

    vote_weight = calc_vote_weight(vote)
    cast_vote(vote_weight, vote_type='new')

    return jsonify(msg='You cast a new vote on this bill.')


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

    user = User.objects.get(email=get_jwt_identity())
    delegate = User.objects.get(id=delegate_id)
    bill = Bill.objects.get(id=bill_id)

    delegated_vote = DelegatedVote(
            delegator=user.id,
            delegate=delegate_id,
            cast_vote=CastVote(bill_id=bill_id))

    for d in user.delegated_votes:
        if d.delegate == delegate.id \
                and d.cast_vote.bill_id == bill.id:
            return jsonify(msg='Already delegated this vote.')
        elif d.cast_vote.bill_id == bill.id:
            print("\nuser.delegated_votes (before): {}\n".format(str(user.delegated_votes)))
            user.delegated_votes.remove(d)
            print("\nuser.delegated_votes (after): {}\n".format(str(user.delegated_votes)))
            print("\ndelegate of bill: {}\n".format(d.delegate))
            old_delegate = User.objects.get(id=d.delegate)
            print("\nold_delegate\n".format(old_delegate.id))
            for d_1 in old_delegate.received_votes:
                print("\nold_delegate's delegate bill: {}\n".format(d_1.cast_vote.bill_id))
                if d_1.cast_vote.bill_id == bill.id \
                        and d_1.delegator == user.id:
                    print("\nold_delegate.received_votes (before): {}\n".format(str(old_delegate.received_votes)))
                    old_delegate.received_votes.remove(d_1)
                    print("\nold_delegate.received_votes (after): {}\n".format(str(old_delegate.received_votes)))
                    break

    user.delegated_votes.append(delegated_vote)
    delegate.received_votes.append(delegated_vote)

    reformatted = '_'.join([word.lower() for word in bill.category.split()])
    vector_dict = user.interest_vector.to_mongo()
    vector_dict[reformatted] -= 1
    min_val = vector_dict[min(vector_dict, key=vector_dict.get)]
    for k in vector_dict.keys():
        vector_dict[k] -= min_val
    user.interest_vector = InterestVector(**vector_dict.to_dict())

    user.save()
    delegate.save()

    return jsonify(msg='success')
