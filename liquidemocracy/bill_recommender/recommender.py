import os
import json
import numpy as np
from mongoengine import connect
from liquidemocracy.models import Bill, User, Location

def find_interests(user):
    """
        Isolates the policy areas which constitute the 70% of the user's L2
        normalized interest vector and returns a list of these policy areas and
        also a list of the remaining policy areas.
    """

    # Calculate L2 norm of the user's interest vector
    norm = np.linalg.norm(user, ord=2)

    # Account for cold-start problem for new users
    if not norm:
        norm = np.float64(1.0)

    # L2 normalize the user's interest vector
    user_norm = user/norm

    # Sort policy areas in decreasing order of user interest
    sorted_user = sorted([(val, cls) for cls, val in enumerate(user_norm)],
                         key=lambda x: x[0], reverse=True)

    # Add policy areas to a list until it's filled with those that constitute
    # 70% of the user's interest.
    index, norm_sum, interests = 0, 0, []
    while norm_sum < 0.7 and index < 16:
        norm_sum += np.sum(np.square(sorted_user[index][0]))
        interests.append(classes[str(sorted_user[index][1])])
        index += 1

    # Put the remaining policy areas into a list containing those which are
    # uninteresting to the user
    non_interests = [classes[str(sorted_user[i][1])]
            for i in range(index, len(sorted_user))]

    return interests, non_interests

def convert_user_location(location):
    """
        Converts the locations of users to lowercase and replaces spaces with
        underscores.
    """

    for k, v in location.items():
        location[k] = '_'.join([s.lower() for s in v.split(' ')])

    return location

def convert_bill_location(user_location, level):
    """
        Creates a location object specific to the user's residence location so
        that the Bill model can be queried for only bills that they are allowed
        to vote on.
    """

    location = {'city': '', 'county': '', 'state': ''}

    if level == 'state':
        location = {
                'city': '',
                'county': '',
                'state': user_location['state']
                }
    elif level == 'county':
        location = {
                'city': '',
                'county': user_location['county'],
                'state': ''
                }
    elif level == 'city':
        location = {
                'city': user_location['city'],
                'county': '',
                'state': ''
                }

    return location

def find_interesting_bills(interests, user_location, filtered_levels):
    """
        Query the Bill model for only those bills whose policy area is of
        interest to the user and is able to be voted on by the user.
    """

    recommended_bills = []
    bill_locations = [convert_bill_location(user_location, level)
            for level in levels]
    recommended_bills += Bill.objects(
            level__in=filtered_levels,
            category__in=interests,
            location__in=bill_locations
            )

    return recommended_bills

def find_delegates(user, non_interests):
    """
        Returns a dictionary keyed by policy areas that are deemed
        uninteresting by the user. Each value is a dictionary keyed by
        governance level. The values of these dictionaries are lists of the
        user's delegates who both are able to vote on these bills (because
        their residence location for that level of governance matches that of
        the user) and have demonstrated interest in the given policy area.
    """

    location_map = {level: [] for level in levels}

    # Populate location_map with the delegates of the user who are able to vote
    # on bills in that location
    for delegate in user.delegates:
        delegate_user = User.objects.get(id=delegate.user_id)
        for level in location_map.keys():

            if level == 'federal':
                delegate_loc = user_loc = 'federal'
            elif level == 'state':
                delegate_loc = delegate_user.residence.location.state
                user_loc = user.residence.location.state
            elif level == 'county':
                delegate_loc = delegate_user.residence.location.county
                user_loc = user.residence.location.county
            elif level == 'city':
                delegate_loc = delegate_user.residence.location.city
                user_loc = user.residence.location.city

            if delegate_loc == user_loc:
                location_map[level].append(delegate_user)

    recommendations_map = {
            policy_area: {level: [] for level in levels}
            for policy_area in non_interests
            }

    # Populate recommendations_map with delegates in location_map who have
    # shown interest in the given policy area.
    for policy_area in non_interests:
        for level in levels:
            for d in location_map[level]:
                d_interest_vector = list(
                        json.loads(d.interest_vector.to_json()).values())
                d_interests, _ = find_interests(d_interest_vector)
                if policy_area in d_interests:
                    recommendations_map[policy_area][level].append(d)

    return recommendations_map

def recommend_bills(user_email, filtered_levels):

    print('operating directoyr is', os.getcwd())
    classes = json.load(open('bill_classifier/class_mapping.json', 'r'))
    levels = ['federal', 'state', 'county', 'city']

    try:
        user = User.objects.get(email=user_email)
    except Exception as e:
        print(e)

    user_location = convert_user_location(
            json.loads(user.residence.location.to_json()))

    interest_vector = [0, 3, 1, 0, 0, 5, 5, 6, 12, 2, 4, 6, 9, 21, 3, 4]
    #interest_vector = list(json.loads(user.interest_vector.to_json()).values())
    interests, non_interests = find_interests(interest_vector)
    recommended_bills = find_interesting_bills(interests, user_location, filtered_levels)

    return recommended_bills

#potential_delegates = find_delegates(user, non_interests)
