import datetime
import dateutil
from flask import Blueprint, request, url_for, render_template, jsonify
from flask import current_app as app
from flask_jwt_simple import jwt_required, get_jwt_identity
from liquidemocracy.models import User, InterestVector, Residence, Location
from liquidemocracy.utils import send_email
from itsdangerous import URLSafeTimedSerializer

account = Blueprint('account', __name__)

@account.route('/api/create_user/', methods=['POST'])
def create_user():
    """
        This endpoint serializes the email and password that the user supplies
        as input, embeds it as a URL parameter in an activation link, and then
        emails this link to the email provided by the user.
    """

    req = request.get_json()
    email = req['email']
    password = req['password']
    name = req['name']
    city = req['city']
    county = req['county']
    state = req['state']

    if not User.exists(email):
        ts = URLSafeTimedSerializer(app.config['SERIALIZATION_KEY'])
        token = ts.dumps(
                {
                    'email': email,
                    'password': password,
                    'name': name,
                    'city': city,
                    'county': county,
                    'state': state
                }, salt='account_creation_key')
        email_url = url_for(
                'account.confirm_account_creation',
                token=token,
                _external=True)
        subject = 'Confirm your Liquidemocracy account'
        html = render_template(
                'account_activation.html',
                email_url=email_url)

        try:
            send_email(email, subject, html)
            return jsonify(msg='Sent account confirmation link to email.')
        except Exception as e:
            print(e)
            return jsonify(error=str(e))

    return jsonify(error='This email is already in use.')


@account.route('/api/create_user/<token>/', methods=['GET'])
def confirm_account_creation(token):
    """
        Upon email confirmation, add new user to the User model.
    """

    #TODO: redirect to React component for login

    try:
        ts = URLSafeTimedSerializer(app.config['SERIALIZATION_KEY'])
        token = ts.loads(token, salt='account_creation_key', max_age=21600)
        if not User.exists(token['email']):
            User(
                 email=token['email'],
                 password=token['password'],
                 name=token['name'],
                 interest_vector=InterestVector(),
                 residence=Residence(
                     location=Location(
                         city=token['city'],
                         county=token['county'],
                         state=token['state']
                         ),
                     last_update=datetime.datetime.now()
                     )
                 ).save()
            return jsonify(msg='Account created.')
        return jsonify(error='This email is already in use.')
    except Exception as e:
        print(e)
        return jsonify('error')


@account.route('/api/reset_password/', methods=['POST'])
def reset_password():
    """
        This endpoint takes in the email address to send the account recovery
        link to as well as the new password. These inputs are serialized and
        embedded in the account recovery link.
    """

    req = request.get_json()
    email = req['email']
    password = req['password']

    if User.exists(email):
        ts = URLSafeTimedSerializer(app.config['SERIALIZATION_KEY'])
        token = ts.dumps(
                {
                    'email': email,
                    'password': password
                }, salt='account_recovery_key')
        email_url = url_for(
                'account.confirm_account_recovery',
                token=token,
                _external=True)
        subject = 'Recover your Liquidemocracy account'
        html = render_template(
                'account_recovery.html',
                email_url=email_url)

        try:
            send_email(email, subject, html)
            return jsonify(msg='Sent account recovery link to email.')
        except Exception as e:
            print(e)
            return jsonify(error=str(e))

    return jsonify(error='There is no user with this email.')


@account.route('/api/reset_password/<token>/', methods=['GET'])
def confirm_account_recovery(token):
    """
        When the user clicks on the account recovery link sent to their email,
        their password is updated to the password embedded in the serialized
        link and the user is redirected to the React component for logging in.
    """

    #TODO: redirect to React component for login

    try:
        ts = URLSafeTimedSerializer(app.config['SERIALIZATION_KEY'])
        token = ts.loads(token, salt='account_recovery_key', max_age=21600)
        user = User.objects.get(email=token['email'])
        user.update(password=token['password'])
        return jsonify(msg='User {} successfully reset their password to {}'.format(token['email'], token['password']))
    except Exception as e:
        return jsonify(error=str(e))


@account.route('/api/profile/update/', methods=['POST'])
@jwt_required
def update_profile():
    """
        This endpoint takes in all the input fields of the profile view. The
        user's name can be updated freely...the residence information can only
        be updated once every 6 months...the email can be updated freely but
        requires confirming the email via a confirmation link.
    """

    req = request.get_json()
    name = req['name']
    email = req['email']
    city = req['city']
    county = req['county']
    state = req['state']

    user = User.objects.get(email=get_jwt_identity())

    if user.email != email:
        if not User.exists(email):
            ts = URLSafeTimedSerializer(app.config['SERIALIZATION_KEY'])
            token = ts.dumps(
                    {
                        'old_email': user.email,
                        'new_email': email
                    }, salt='update_email_key')
            email_url = url_for(
                    'account.confirm_update_email',
                    token=token,
                    _external=True)
            subject = 'Confirm updating your Liquidemocracy email'
            html = render_template(
                    'email_update.html',
                    email_url=email_url)
            try:
                send_email(email, subject, html)
            except Exception as e:
                print(e)
        else:
            print('This email is already in use.')

    last_update = user.residence.last_update
    location = user.residence.location
    now = datetime.datetime.now()
    if city.lower() != location.city.lower() \
            or county.lower() != location.county.lower() \
            or state.lower() != location.state.lower():
                print("\nnew city: {}  --  old city: {}\nnew county: {}  -- old county: {}\nnew state: {}  --  old state: {}\n".format(
                    city.lower(), location.city.lower(),
                    county.lower(), location.county.lower(),
                    state.lower(), location.state.lower()))

                print("\nlast update: {}\nstr(last update): {}\nnow: {}\nparsed last update: {}\n".format(
                    last_update, str(last_update), str(now),
                    dateutil.parser.parse(str(last_update))))
        #user.update(city=city, county=county, state=state)

    #user.update(name=name)

    return jsonify(msg='Successfully updated user profile information.')


@account.route('/api/profile/update/<token>/', methods=['GET'])
def confirm_update_email(token):
    """
        This is the endpoint that actually updates the user's email after
        confirming their new email address.
    """

    try:
        ts = URLSafeTimedSerializer(app.config['SERIALIZATION_KEY'])
        token = ts.loads(token, salt='update_email_key', max_age=21600)
        if not User.exists(token['new_email']):
            user = User.objects.get(email=token['old_email'])
            user.update(email=token['new_email'])
            return jsonify(msg='Account email updated.')
        return jsonify(error='This email is already in use.')
    except Exception as e:
        return jsonify(error=str(e))


@account.route('/api/profile/', methods=['GET'])
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
        'city': user.residence.location.city,
        'county': user.residence.location.county,
        'state': user.residence.location.state,
        }

    return jsonify(res)
