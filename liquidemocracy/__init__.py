from flask import Flask
from flask_cors import CORS
from flask_jwt_simple import JWTManager
from liquidemocracy.models import db
from liquidemocracy.views.account import account
from liquidemocracy.views.active_votes import active_votes
from liquidemocracy.views.bill import bill
from liquidemocracy.views.bill_list import bill_list

def create_app():
    app = Flask(__name__)
    app.config.from_object('liquidemocracy.app_config.DevelopmentConfig')
    CORS(app, resources=r'/api/*')
    jwt = JWTManager(app)

    db.init_app(app)

    app.register_blueprint(account)
    app.register_blueprint(active_votes)
    app.register_blueprint(bill)
    app.register_blueprint(bill_list)

    return app

app = create_app()
