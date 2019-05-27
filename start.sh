#!/bin/bash

ENV=${1:-development}

export FLASK_ENV=${ENV}
FLASK_APP="call_receiver.app:create_app()" flask run
