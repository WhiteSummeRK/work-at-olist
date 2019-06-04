from flask import Blueprint, jsonify, request
from call_receiver.serealizer import PhoneCallReceive

app = Blueprint('receive', __name__)


@app.route('/', methods=['POST'])
def receive_data():
    pcr = PhoneCallReceive()
    result, error = pcr.load(request.json)


    if error:
        return jsonify(error), 400

    return pcr.jsonify(result), 201
