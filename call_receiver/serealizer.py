from datetime import datetime
from flask_marshmallow import Marshmallow
from marshmallow.validate import Length, OneOf
from marshmallow import validates, ValidationError, validates_schema, fields, pre_load

from call_receiver.models import CallRecord, Bill


ma = Marshmallow()


def configure(app):
    ma.init_app(app)


class PhoneCallReceive(ma.ModelSchema):
    class Meta:
        model = CallRecord

    record_type = fields.Int(
        required=True,
        validate=OneOf(
            choices=[0, 1],
            error='Err: record_type is 0 for start call and 1 for end call')
    )
    record_timestamp = fields.Str(required=True)
    call_identifier = fields.Int(required=True)
    origin_phone = fields.Str(
        required=False,
        validate=Length(
            min=10,
            max=11,
            error='Err: origin_phone should be min={min} and max={max}'
        )
    )
    dest_phone = fields.Str(
        required=False,
        validate=Length(
            min=10,
            max=11,
            error='Err: dest_phone should be min={min} and max={max}'
        )
    )

    @pre_load
    def check_phone_numbers(self, data):
        dest_status = 'dest_phone' in data.keys()
        orig_status = 'origin_phone' in data.keys()
        record_type = data.get('record_type')
        if record_type == 1 and any([dest_status, orig_status]):
            raise ValidationError(
                'Err: Phone numbers are not necessary for end calls',
                'phone_validation'
            )
        if record_type == 0 and not all([dest_status, orig_status]):
            raise ValidationError(
                'Err: Please, pass the phone numbers',
                'phone_validation'
            )


class GetBill(ma.ModelSchema):
    class Meta:
        model = Bill

    sub_number = fields.Str(required=True)
    reference_period = fields.Str(required=False)
