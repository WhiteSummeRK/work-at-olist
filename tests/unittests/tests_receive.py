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
        test = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
        request = self.client.post(
            url_for('receive.receive_data'),
            json={
                'record_type': 0,
                'record_timestamp': test,
                'call_identifier': 30,
                'origin_phone': '1231231231',
                'dest_phone': '0'}
        )

        expected = {
            'dest_phone': ['Error: dest_phone format is incorrect']
        }

        self.assertEqual(request.status_code, 400)
        self.assertEqual(request.json['dest_phone'], expected['dest_phone'])

    def tests_receive_should_respond_400_when_origin_phone_is_incorrect(self):
        test = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
        request = self.client.post(
            url_for('receive.receive_data'),
            json={
                'record_type': 1,
                'record_timestamp': test,
                'call_identifier': 30,
                'origin_phone': '0',
                'dest_phone': '1231231231'}
        )

        expected = {
            'origin_phone': ['Error: origin_phone format is incorrect']
        }

        self.assertEqual(request.status_code, 400)
        self.assertEqual(
            request.json['origin_phone'],
            expected['origin_phone']
        )

    def tests_receive_data_should_respond_201_when_payload_is_correct(self):
        test = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
        request = self.client.post(
            url_for('receive.receive_data'),
            json={
                'record_type': 0,
                'record_timestamp': test,
                'call_identifier': 30,
                'origin_phone': '1234567891',
                'dest_phone': '12345678911'}
        )
        self.assertEqual(request.status_code, 201)

    @patch('call_receiver.controllers.routes.receive.save_call')
    def tests_receive_data_should_call_sqlalchemy(self, save_mock):
        test = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
        request = self.client.post(
            url_for('receive.receive_data'),
            json={
                'record_type': 1,
                'record_timestamp': test,
                'call_identifier': 30,
                'origin_phone': '1234567891',
                'dest_phone': '12345678911'}
        )
        self.assertTrue(save_mock.called)
