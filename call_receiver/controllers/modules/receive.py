from call_receiver.models import CallRecord
from datetime import datetime
from flask import current_app


def save_call(call_data):
    try:
        data = CallRecord(
            record_type=call_data['record_type'],
            call_identifier=call_data['call_identifier'],
            record_timestamp=call_data['record_timestamp'],
            origin_phone=call_data['origin_phone'],
            dest_phone=call_data['dest_phone']
            )
        current_app.db.session.add(data)
        current_app.db.session.commit()
        return data
    except Exception as e:
        current_app.db.session.rollback()
        current_app.db.session.remove()
        return e
