from flask import Blueprint, request, url_for, render_template, jsonify
from flask_jwt_simple import jwt_required, get_jwt_identity
from flask import current_app as app
from liquidemocracy.models import User
from liquidemocracy.utils import send_email
from itsdangerous import URLSafeTimedSerializer

profile = Blueprint('profile', __name__)

@profile.route('/api/profile/update/', methods=['POST'])
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
                    'profile.confirm_update_email',
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

    # if city, county, and state haven't changed in the last 6 months:
    user.update(city=city, county=county, state=state)

    user.update(name=name)

    return jsonify(msg='Successfully updated user profile information.')


@profile.route('/api/profile/update/<token>/', methods=['GET'])
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
