from flask import Flask
from flask_cors import CORS
from flask_jwt_simple import JWTManager
from liquidemocracy.models import db
from liquidemocracy.views.account import account
from liquidemocracy.views.menu import menu
from liquidemocracy.views.profile import profile
from liquidemocracy.views.active_votes import active_votes
from liquidemocracy.views.bill_list import bill_list
from liquidemocracy.views.bill import bill

def create_app():
    app = Flask(__name__)
    app.config.from_object('liquidemocracy.app_config.DevelopmentConfig')
    CORS(app, resources=r"/api/*")
    jwt = JWTManager(app)

    db.init_app(app)

    app.register_blueprint(account)
    app.register_blueprint(menu)
    app.register_blueprint(profile)
    app.register_blueprint(active_votes)
    app.register_blueprint(bill_list)
    app.register_blueprint(bill)

    return app

app = create_app()
