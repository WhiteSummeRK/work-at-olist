"""WIP"""
from datetime import datetime
from decimal import Decimal
from flask import current_app

from call_receiver.models import CallRecord

STANDING_CHARGE = 0.36
BEFORE_22_CHARGE = 0.09
AFTER_22_CHARGE = 0.00
APPLIED_AFTER = 60


def format_date(date):
    """Return date format as YYYY/MM/DD based on a given timestamp."""
    return datetime.fromtimestamp(date).strftime('%Y/%m/%d')


def format_time(time):
    """Return time format as HH/MM/SS based on a given timestamp."""
    return datetime.fromtimestamp(time).strftime('%H:%M:%S')


def calculate_duration(time_1, time_2, return_delta=False):
    """Return duration between two timestamps."""
    delta_1 = datetime.fromtimestamp(time_1)
    delta_2 = datetime.fromtimestamp(time_2)

    if delta_1 > delta_2:
        result = delta_1 - delta_2
    else:
        result = delta_2 - delta_1

    return result if return_delta else str(result)


def calculate_price(duration, time_1, time_2):
    """WIP"""
    delta_1 = datetime.fromtimestamp(time_1)
    delta_2 = datetime.fromtimestamp(time_2)

    if duration.seconds > APPLIED_AFTER:
        times_to_charge = duration.seconds // APPLIED_AFTER

        return float('{0:.2f}'.format(
            STANDING_CHARGE + times_to_charge * BEFORE_22_CHARGE
        ))

    return STANDING_CHARGE


def save_call(data):
    """
    Receives de data passed by marshmallow and use the module functions
    to save it into the database

        data -> Marshmallow result json
    """
    error = None

    try:
        call = CallRecord(
            destination=data['destination'],
            call_start_date=data['call_start_date'],
            call_start_time=data['call_start_time'],
            call_duration=data['call_duration'],
            call_price=data['call_price'],
            bill=data['bill']
        )

        current_app.db.session.add(call)
        current_app.db.session.commit()

        return call, error
    except Exception:
        current_app.db.session.remove()
        current_app.db.session.rollback()

        err_msg = {
            'database_error': [
                'Err: Something wents wrong while inserting into database']
        }

        return None, err_msg
