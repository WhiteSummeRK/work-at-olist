"""Tables module"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def configure(app):
    db.init_app(app)
    app.db = db


class CallReceiver(db.Model):
    __tablename__ = 'call_receiver'

    id = db.Column(db.Integer, primary_key=True)
    record_type = db.Column(db.String(300))
    record_timestamp = db.Column(db.String(300))
    call_identifier = db.Column(db.String(300))
    origin_phone = db.Column(db.String(300))
    dest_phone = db.Column(db.String(300))
