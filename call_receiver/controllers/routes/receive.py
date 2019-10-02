from flask import Blueprint, jsonify, request
from call_receiver.serealizer import PhoneCallReceive
from call_receiver.controllers.modules.receive import save_call
from marshmallow import ValidationError


app = Blueprint('receive', __name__)


@app.route('/', methods=['POST'])
def receive_data():
    pcr = PhoneCallReceive()

    try:
        result = pcr.load(request.json)
    except ValidationError as err:
        return jsonify(err.normalized_messages()), 400

    _, error_call = save_call(result)

    if error_call:
        return jsonify(error_call), 400

    return pcr.jsonify(result), 201
