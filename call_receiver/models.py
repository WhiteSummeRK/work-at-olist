"""Tables module"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def configure(app):
    db.init_app(app)
    app.db = db


class CallReceiver(db.Model):
    __tablename__ = 'call_receiver'

    id = db.Column(db.Integer, primary_key=True)
    record_type = db.Column(db.Integer, nullable=False)
    record_timestamp = db.Column(db.DateTime, nullable=False)
    call_identifier = db.Column(db.Integer, nullable=False)
    origin_phone = db.Column(db.String(300))
    dest_phone = db.Column(db.String(300))

    def __repr__(self):
        type_to_show = {
            0: "Call Start Record",
            1: "Call End Record"
        }

        return 'CallReceiver(record_type={}, record_timestamp={}, \
        call_identifier={}, origin_phone={}, dest_phone={})'.format(
            type_to_show[self.record_type], self.record_timestamp,
            self.call_identifier, self.origin_phone, self.dest_phone
        )
