from flask_marshmallow import Marshmallow
from marshmallow import fields, validates, ValidationError, validates_schema
from call_receiver.models import CallReceiver


ma = Marshmallow()


def configure(app):
    ma.init_app(app)


class PhoneCallReceive(ma.ModelSchema):
    class Meta:
        model = CallReceiver

    record_type = fields.Str(required=True)
    record_timestamp = fields.Str(required=True)
    call_identifier = fields.Int(required=True)
    origin_phone = fields.Str(required=True)
    dest_phone = fields.Str(required=True)

    @validates_schema
    def validate_origin_phone(self, data):
        if len(data['dest_phone']) not in [10, 11]:
            raise ValidationError("Error: dest_phone format is incorrect",
                                  "dest_phone")
        if len(data['origin_phone']) not in [10, 11]:
            raise ValidationError("Error: origin_phone format is incorrect",
                                  "origin_phone")
