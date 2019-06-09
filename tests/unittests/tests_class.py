from unittest import TestCase, mock
from call_receiver.app import create_app
from call_receiver.controllers.routes import receive
from datetime import datetime


class BaseRouteTests(TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client()

        receive.save_call = mock.MagicMock(return_value=(True, False))

        self.date_test = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')

    def tearDown(self):
        pass
