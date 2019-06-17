"""WIP"""
from datetime import datetime, timedelta, date, time
from decimal import Decimal
from flask import current_app
import math

from call_receiver.models import CallRecord

STANDING_CHARGE = 0.36
BEFORE_22_CHARGE = 0.09
AFTER_22_CHARGE = 0.00
MININUM_DURATION = 60


def format_date(date):
    """Return date format as YYYY/MM/DD based on a given timestamp."""
    return datetime.fromtimestamp(date).strftime('%Y/%m/%d')


def format_time(time):
    """Return time format as HH/MM/SS based on a given timestamp."""
    return datetime.fromtimestamp(time).strftime('%H:%M:%S')


def in_between(time, start, end):
    """Check if the given time is between two other times."""
    if start <= end:
        return start <= time < end
    return start <= time or time < end


def calculate_duration(time_1, time_2, return_delta=False):
    """Return duration between two timestamps."""
    delta_1 = datetime.fromtimestamp(time_1)
    delta_2 = datetime.fromtimestamp(time_2)

    if delta_1 > delta_2:
        result = delta_1 - delta_2
    else:
        result = delta_2 - delta_1

    return result if return_delta else str(result)


def minutes_to_22(input_time):
    """Calculate the amount of minutes before 22PM."""
    _22H = datetime.combine(date.min, time(22))
    to_sub = datetime.combine(date.min, input_time.time())

    return math.ceil((_22H - to_sub).total_seconds() / 60)


def minutes_after_6(input_time):
    """Calculate the amount of minutes after 6AM."""
    _6H = datetime.combine(date.min, time(6))
    to_sub = datetime.combine(date.min, input_time.time())

    return (to_sub - _6H).total_seconds() // 60


def calculate_price(duration, time_1, time_2):
    """
    Calculate price and Hold all pricing rules.

    TODO: this function should be refactored to fit into CC A

        duration => call duration
        time_1 => the time of the start call
        time_2 => the time of the end call

        returns => Float => a value containing the price of the call.
    """
    delta_1 = datetime.fromtimestamp(time_1)
    delta_2 = datetime.fromtimestamp(time_2)

    if duration.seconds > MININUM_DURATION:
        times_to_charge = duration.seconds // MININUM_DURATION

        # scenario 01
        if in_between(delta_1.hour, 22, 6) and in_between(delta_2.hour, 22, 6):
            return float('{0:.2f}'.format(
                STANDING_CHARGE + times_to_charge * AFTER_22_CHARGE
            ))

        # scenario 02
        if in_between(delta_1.hour, 6, 22) and in_between(delta_2.hour, 6, 22):
            return float('{0:.2f}'.format(
                STANDING_CHARGE + times_to_charge * BEFORE_22_CHARGE
            ))

        # scenário 03
        if in_between(delta_1.hour, 6, 22) and in_between(delta_2.hour, 22, 6):
            times_before_22 = minutes_to_22(delta_1)

            return float('{0:.2f}'.format(
                STANDING_CHARGE + (times_to_charge - times_before_22)
                * BEFORE_22_CHARGE
            ))

        # scenario 04
        if in_between(delta_1.hour, 22, 6) and in_between(delta_2.hour, 6, 22):
            times_after_6 = minutes_after_6(delta_2)

            return float('{0:.2f}'.format(
                STANDING_CHARGE + (times_to_charge - times_after_6)
                * BEFORE_22_CHARGE
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
