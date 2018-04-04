import datetime
from flask import Blueprint, request, url_for, render_template, jsonify
from flask import current_app as app
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

    print('\nemail: {}\npassword: {}\nname: {}\ncity: {}\ncounty: {}\nstate: {}\n'.format(
        email, password, name, city, county, state
        ))

    if not User.exists(email):
        print('\nUser does not already exist\n')
        ts = URLSafeTimedSerializer(app.config['SERIALIZATION_KEY'])
        print('\nserializer created\n')
        token = ts.dumps(
                {
                    'email': email,
                    'password': password,
                    'name': name,
                    'city': city,
                    'county': county,
                    'state': state
                }, salt='account_creation_key')
        print('\ntoken created\n')
        email_url = url_for(
                'account.confirm_account_creation',
                token=token,
                _external=True)
        print('\nemail url created\n')
        subject = 'Confirm your Liquidemocracy account'
        html = render_template(
                'account_activation.html',
                email_url=email_url)
        print('\nhtml template created\n')

        try:
            print('\nbefore send email\n')
            send_email(email, subject, html)
            print('\nafter send email\n')
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
