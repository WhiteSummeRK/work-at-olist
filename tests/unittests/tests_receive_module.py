from unittest import TestCase, mock
from datetime import datetime

from call_receiver.app import create_app
from call_receiver.controllers.modules.receive import (format_date,
                                                       format_time,
                                                       calculate_duration,
                                                       calculate_price)


class BaseModulesTest(TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/call_r.db'

        self.app.db.create_all()

    def tearDown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()

    def test_format_date_should_return_correct_date_YYYY_MM_DD(self):
        date = 1545730073
        result = format_date(date)

        self.assertEqual(result, '2018/12/25')

    def test_format_time_should_return_correct_time_YYYY_MM_DD(self):
        time = 1545730073
        result = format_time(time)

        self.assertEqual(result, '07:27:53')

    def test_calculate_duration_should_calculate_correctly(self):
        time_1 = 1545730073
        time_2 = 1545730173

        expected = '0:01:40'

        result = calculate_duration(time_1, time_2)

        self.assertEqual(result, expected)

    def test_calculate_duration_should_operate_subtracting_lower_nums(self):
        time_1 = 1545730073
        time_2 = 1545730173

        expected = '0:01:40'

        result = calculate_duration(time_2, time_1)

        self.assertEqual(result, expected)

    def test_calculate_price_should_return_correct_price(self):
        time_1 = 1545730073
        time_2 = 1545730173

        result = calculate_price(
            calculate_duration(time_1, time_2, return_delta=True),
            time_1,
            time_2
        )

        self.assertEqual(result, 0.45)
