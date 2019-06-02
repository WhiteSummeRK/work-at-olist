"""Start flask app."""
from flask import Flask
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate


def create_app():
    app = Flask(__name__)

    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config.from_object('call_receiver.config.DevelopmentConfig')

    from call_receiver.models import configure as config_db
    config_db(app)

    from call_receiver.serealizer import configure as config_mm
    config_mm(app)

    Migrate(app, app.db)
    # Blueprints
    from call_receiver.controllers.routes.receive import app as receive
    app.register_blueprint(receive, url_prefix='/')

    return app
