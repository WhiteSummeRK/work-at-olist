from flask import Blueprint, jsonify, request
from call_receiver.serealizer import GetBill
from call_receiver.controllers.modules.receive import save_call

app = Blueprint('bill', __name__)


@app.route('/')
def get_bill():
    bill = GetBill()

    result, error = bill.load(request.json)

    return jsonify(
        {"not_found": "Error: subscriber number does not exists"}
    ), 201
