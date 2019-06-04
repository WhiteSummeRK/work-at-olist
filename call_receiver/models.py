"""Tables module"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def configure(app):
    db.init_app(app)
    app.db = db


class CallRecord(db.Model):
    __tablename__ = 'call_record'

    id = db.Column(db.Integer, primary_key=True)
    record_type = db.Column(db.Integer, nullable=True)
    record_timestamp = db.Column(db.DateTime, nullable=True)
    call_identifier = db.Column(db.Integer, nullable=True)
    origin_phone = db.Column(db.String(12), nullable=False)
    dest_phone = db.Column(db.String(12), nullable=False)

    def __repr__(self):
        type_to_show = {
            0: "Call Start Record",
            1: "Call End Record"
        }

        return 'CallRecord(record_type={}, record_timestamp={}, \
        call_identifier={}, origin_phone={}, dest_phone={})'.format(
            type_to_show[self.record_type], self.record_timestamp,
            self.call_identifier, self.origin_phone, self.dest_phone
        )


class Bill(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sub_number = db.Column(db.String(12))
    reference_period = db.Column(db.DateTime, nullable=True)
