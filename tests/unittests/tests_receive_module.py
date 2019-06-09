from unittest import TestCase, mock
from datetime import datetime

from call_receiver.app import create_app
from call_receiver.models import Bill, CallRecord
from call_receiver.controllers.modules.receive import (format_date,
                                                       format_time,
                                                       calculate_duration,
                                                       calculate_price,
                                                       save_call)


class BaseModulesTest(TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/call_r.db'

        self.app.db.create_all()

        self.time_for_test_1 = 1545730073
        self.time_for_test_2 = 1545730173

        self.app.db.session.add(Bill(sub_number='9999999999'))
        self.app.db.session.add(Bill(sub_number='12312312312',
                                     reference_period='2019/03/02'))
        self.app.db.session.commit()

        self.bill_w_period = Bill.query.order_by(Bill.id.desc()).first()
        self.bill_w_no_period = Bill.query.first()

    def tearDown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()

    def test_format_date_should_return_correct_date_YYYY_MM_DD(self):
        date = 1545730073
        result = format_date(date)

        self.assertEqual(result, '2018/12/25')

    def test_format_time_should_return_correct_time_YYYY_MM_DD(self):
        result = format_time(self.time_for_test_1)

        self.assertEqual(result, '07:27:53')

    def test_calculate_duration_should_calculate_correctly(self):
        expected = '0:01:40'

        result = calculate_duration(self.time_for_test_1, self.time_for_test_2)

        self.assertEqual(result, expected)

    def test_calculate_duration_should_operate_subtracting_lower_nums(self):
        expected = '0:01:40'

        result = calculate_duration(self.time_for_test_2, self.time_for_test_1)

        self.assertEqual(result, expected)

    def test_calculate_price_should_return_correct_price(self):
        price = 0.45

        result = calculate_price(
            calculate_duration(
                self.time_for_test_1,
                self.time_for_test_2,
                return_delta=True),
            self.time_for_test_1,
            self.time_for_test_2
        )

        self.assertEqual(result, price)

    def test_save_call_function_should_save_data_into_database(self):
        result = save_call({
            "destination": "1234567891",
            "call_start_date": "2018/12/25",
            "call_start_time": "3:50:00",
            "call_duration": "0:10:25",
            "call_price": 25.50,
            "bill": self.bill_w_no_period
        })

        expected = CallRecord.query.filter_by(call_price=25.50).first()

        self.assertTrue(expected)

    def test_save_call_function_should_return_error(self):
        result = save_call({
            "destination": ['invalid_list_and_type'],
            "call_start_date": ['invalid_list_and_type'],
            "call_start_time": ['invalid_list_and_type'],
            "call_duration": ['invalid_list_and_type'],
            "call_price": ['invalid_list_and_type'],
            "bill": ['invalid_list_and_type']
        })

        expected = (None, {'database_error': [
                'Err: Something wents wrong while inserting into database']})

        self.assertEqual(expected, result)
