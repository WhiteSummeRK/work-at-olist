"""Tables module"""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def configure(app):
    db.init_app(app)
    app.db = db


class CallRecord(db.Model):
    __tablename__ = 'call_record'

    id = db.Column(db.Integer, primary_key=True)
    destination = db.Column(db.String(12), nullable=False)
    call_start_date = db.Column(db.String(10), nullable=False)
    call_start_time = db.Column(db.String(10), nullable=False)
    call_duration = db.Column(db.String(10), nullable=False)
    call_price = db.Column(db.Float, nullable=False)
    id_bill = db.Column(db.Integer, db.ForeignKey('bill.id'))
    bill = db.relationship('Bill')

    def __repr__(self):
        return 'CallRecord(destination={}, call_start_date={}, \
        call_start_time={}, call_duration={}, call_price={})'.format(
            self.destination, self.call_start_date,
            self.call_start_time, self.call_duration, self.call_price
        )


class Bill(db.Model):
    __tablename__ = 'bill'

    id = db.Column(db.Integer, primary_key=True)
    sub_number = db.Column(db.String(12))
    reference_period = db.Column(db.DateTime, nullable=True)
