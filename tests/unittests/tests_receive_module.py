from unittest import TestCase, mock
from datetime import datetime

from call_receiver.app import create_app
from call_receiver.controllers.modules.receive import save_call


class BaseModulesTest(TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.testing = True
        self.app_context = self.app.test_request_context()
        self.app_context.push()
        self.client = self.app.test_client()
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/call_r.db'

        self.app.db.create_all()

        self.default_call = {
            'record_type': 0,
            'record_timestamp': datetime.now(),
            'call_identifier': 30,
            'origin_phone': '1234567891',
            'dest_phone': '12345678911'
        }

    def tearDown(self):
        self.app.db.session.remove()
        self.app.db.drop_all()

    @mock.patch('flask.current_app.db.session.add')
    @mock.patch('flask.current_app.db.session.commit')
    def test_save_call_should_save_into_database_correctly(self, add, commit):
        result = save_call(self.default_call)

        self.assertEqual(result.record_type, 0)
        self.assertEqual(result.call_identifier, 30)
        self.assertEqual(result.origin_phone, '1234567891')
        self.assertEqual(result.dest_phone, '12345678911')
        self.assertTrue(add.called)
        self.assertTrue(commit.called)

    @mock.patch('flask.current_app.db.session.rollback')
    @mock.patch('flask.current_app.db.session.remove')
    def test_save_call_should_exc_when_data_is_wrong(self, rollb, remove):
        result = save_call('Super Magnanimous Test')
        self.assertTrue(rollb.called)
        self.assertTrue(remove.called)
