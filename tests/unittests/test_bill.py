from flask import url_for
from datetime import datetime
from tests_class import BaseRouteTests


class TestBillRoute(BaseRouteTests):
    def test_bill_test_should_return_200_when_data_is_passed_correctly(self):
        period = datetime.now().strftime('%Y-%m-%dT%H:%M:%S%z')
        request = self.client.get(
            url_for('bill.get_bill'),
            json={
                "sub_number": '19123123123',
                "reference_period": period}
        )

        expected = {
            'not_found': ['Error: subscriber number does not exists']
        }
        self.assertEqual(request.status_code, 201)
        self.assertEqual(expected['not_found'][0], request.json['not_found'])
