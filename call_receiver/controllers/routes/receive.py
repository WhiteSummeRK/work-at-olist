from flask import Blueprint, jsonify, request
from call_receiver.serealizer import PhoneCallReceive
from call_receiver.controllers.modules.receive import save_call

app = Blueprint('receive', __name__)


@app.route('/', methods=['POST'])
def receive_data():
    pcr = PhoneCallReceive()
    result, error = pcr.load(request.json)
    result_call, error_call = save_call(result)

    if error or error_call:
        return jsonify(error or error_call), 400

    return pcr.jsonify(result), 201
