from flask import url_for
from datetime import datetime
from unittest.mock import patch

from tests_class import BaseRouteTests


class TestsReceiveRoute(BaseRouteTests):
    def tests_receive_should_respond_400_when_payload_is_missing_fields(self):
        request = self.client.post(
            url_for('receive.receive_data'),
            json={
                "origin_phone": '12312312345',
                "dest_phone": '12312312312'}
        )

        expected = {
            'record_timestamp': ['Missing data for required field.'],
            'record_type': ['Missing data for required field.']
        }
        self.assertEqual(request.status_code, 400)
        self.assertEqual(request.json['record_timestamp'],
                         expected['record_timestamp'])
        self.assertEqual(request.json['record_type'],
                         expected['record_type'])

    def tests_receive_should_respond_400_when_dest_phone_is_incorrect(self):
        date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
        request = self.client.post(
            url_for('receive.receive_data'),
            json={
                'record_type': 0,
                'record_timestamp': date,
                'call_identifier': 30,
                'origin_phone': '1231231231',
                'dest_phone': '0'}
        )

        expected = {
            'dest_phone': ['Err: dest_phone should be min=10 and max=11']
        }

        self.assertEqual(request.status_code, 400)
        self.assertEqual(request.json['dest_phone'], expected['dest_phone'])

    def tests_receive_should_respond_400_when_origin_phone_is_incorrect(self):
        date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
        request = self.client.post(
            url_for('receive.receive_data'),
            json={
                'record_type': 0,
                'record_timestamp': date,
                'call_identifier': 30,
                'origin_phone': '0',
                'dest_phone': '1231231231'}
        )

        expected = {
            'origin_phone': ['Err: origin_phone should be min=10 and max=11']
        }

        self.assertEqual(request.status_code, 400)
        self.assertEqual(
            request.json['origin_phone'],
            expected['origin_phone']
        )

    def tests_receive_data_should_respond_201_when_payload_is_correct(self):
        date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
        request = self.client.post(
            url_for('receive.receive_data'),
            json={
                'record_type': 0,
                'record_timestamp': date,
                'call_identifier': 30,
                'origin_phone': '1234567891',
                'dest_phone': '12345678911'}
        )
        self.assertEqual(request.status_code, 201)

    @patch('call_receiver.controllers.routes.receive.save_call')
    def tests_receive_data_should_call_sqlalchemy(self, save_mock):
        date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
        request = self.client.post(
            url_for('receive.receive_data'),
            json={
                'record_type': 0,
                'record_timestamp': date,
                'call_identifier': 30,
                'origin_phone': '1234567891',
                'dest_phone': '12345678911'}
        )
        self.assertTrue(save_mock.called)

    def test_receive_data_should_respond_400_when_record_type_incorrect(self):
        date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
        request = self.client.post(
            url_for('receive.receive_data'),
            json={
                'record_type': 2,
                'record_timestamp': date,
                'call_identifier': 30,
                'origin_phone': '1234567891',
                'dest_phone': '12345678911'}
        )
        self.assertEqual(request.status_code, 400)
        self.assertEqual(
            request.json['record_type'][0],
            "Err: record_type is 0 for start call and 1 for end call"
        )

    def test_respond_400_with_origin_phone_field_and_call_end_record(self):
        date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
        request = self.client.post(
            url_for('receive.receive_data'),
            json={
                'record_type': 1,
                'record_timestamp': date,
                'call_identifier': 30,
                'origin_phone': '1234567891'
            }
        )
        self.assertEqual(request.status_code, 400)
        self.assertEqual(
            request.json['phone_validation'][0],
            "Err: Phone numbers are not necessary for end calls"
        )

    def test_respond_400_with_dest_phone_field_and_call_end_record(self):
        date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
        request = self.client.post(
            url_for('receive.receive_data'),
            json={
                'record_type': 1,
                'record_timestamp': date,
                'call_identifier': 30,
                'dest_phone': '1234567891'
            }
        )
        self.assertEqual(request.status_code, 400)
        self.assertEqual(
            request.json['phone_validation'][0],
            "Err: Phone numbers are not necessary for end calls"
        )

    def test_should_responde_201_when_no_phone_with_end_call(self):
        date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
        request = self.client.post(
            url_for('receive.receive_data'),
            json={
                'record_type': 1,
                'record_timestamp': date,
                'call_identifier': 30,
            }
        )
        self.assertEqual(request.status_code, 201)

    def test_should_respond_400_when_no_phone_with_start_call(self):
        date = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
        request = self.client.post(
            url_for('receive.receive_data'),
            json={
                'record_type': 0,
                'record_timestamp': date,
                'call_identifier': 30,
            }
        )

        expected = 'Err: Please, pass the phone numbers'

        self.assertEqual(request.status_code, 400)
        self.assertEqual(request.json['phone_validation'][0], expected)
