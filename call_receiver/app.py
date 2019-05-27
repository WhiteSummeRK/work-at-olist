"""Start flask app."""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    # imports

    # Flask application and needed setups
    app = Flask(__name__)

    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    app.config.from_object('call_receiver.config.DevelopmentConfig')

    db.init_app(app)

    # Blueprints

    from call_receiver.controllers.routes.example import app as example
    app.register_blueprint(example, url_prefix='/')

    return app
