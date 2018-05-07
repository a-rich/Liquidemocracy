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

    if delegate.id == user.id:
        return jsonify(msg="You can not add yourself as a delegate")

    delegate_obj = Delegate(user_id=delegate.id, name=delegate.name)
    user.delegates.append(delegate_obj)
    user.save()

    return jsonify(msg="Successfully added {} to {}'s delegates list".format(
            delegate.name, user.name))

@active_votes.route('/api/delegate/remove/', methods=['POST'])
@jwt_required
def remove_delegate():
    """
    """

    req = request.get_json()
    User.objects(email=get_jwt_identity()).update_one(pull__delegates__user_id=req['delegate_id'])

    return jsonify(msg="Successfully removed delegate")

@active_votes.route('/api/category/delegate/', methods=['POST'])
@jwt_required
def delegate():
    """
    """

    req = request.get_json()
    category = req['category']
    delegate_id = req['delegate_id']

    user = User.objects.get(email=get_jwt_identity())
    delegate = User.objects.get(id=delegate_id)
    delegated_category = DelegatedCategory(
            delegator=user.id,
            delegate=delegate_id,
            category=category)

    for d in user.delegated_categories:
        if d.delegate == delegate.id \
                and d.category == category:
            return jsonify(msg='Already delegated this category.')
        elif d.category == category:
            user.delegated_cateogries.remove(d)
            old_delegate = User.objects.get(id=d.delegate)
            for d_1 in old_delegate.received_categories:
                if d_1.category == category \
                        and d_1.delegator == user.id:
                    old_delegate.received_categories.remove(d_1)
                    old_delegate.save()
                    break

    user.delegated_categories.append(delegated_category)
    delegate.received_categories.append(delegated_category)
    for d in user.delegates:
        if d.user_id == delegate.id:
            d.categories.append(category)

    reformatted = '_'.join([word.lower().replace(',', '') for word in category.split()])
    vector_dict = user.interest_vector.to_mongo()
    vector_dict[reformatted] -= 1
    min_val = vector_dict[min(vector_dict, key=vector_dict.get)]
    for k in vector_dict.keys():
        vector_dict[k] -= min_val
    user.interest_vector = InterestVector(**vector_dict.to_dict())

    user.save()
    delegate.save()

    return jsonify(msg="Success")

@active_votes.route('/api/remove/delegation/', methods=['POST'])
@jwt_required
def remove_delegation():

     req = request.get_json()
     bill_id = req['bill_id']
     delegate_id = req['delegate']

     user = User.objects.get(email=get_jwt_identity())
     delegate = User.objects.get(id=delegate_id)
     bill = Bill.objects.get(id=bill_id)

     for d in user.delegated_votes:
         if d.delegate == delegate.id \
                 and d.cast_vote.bill_id == bill.id:
            user.delegated_votes.remove(d)
            delegate = User.objects.get(id=d.delegate)
            for d_1 in delegate.received_votes:
                if d_1.cast_vote.bill_id == bill.id \
                        and d_1.delegator == user.id:
                    delegate.received_votes.remove(d_1)
                    delegate.save()
                    break

     for d in user.delegates:
         if d.user_id == delegate.id:
             for bill_ in d.bills:
                 if str(bill_.bill_id) == str(bill.id):
                    d.bills.remove(bill_)

     user.save()
     delegate.save()

     return jsonify(msg='success')

@active_votes.route('/api/votes/active/', methods=['GET'])
@jwt_required
def votes_active():

    user = User.objects.get(email=get_jwt_identity())

    return jsonify(user.delegates)
