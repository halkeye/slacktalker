import unittest
import requests_mock
from mock import patch
from .web import app
from .db import db


class WebTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        app.debug = True
        with app.app_context():
            db.create_all()

    def tearDown(self):
        pass

    def test_root(self):
        rv = self.app.get('/')
        self.assertEqual(200, rv.status_code)
 
    @patch('slack_resurrect.main.SLACK_CLIENT.chat_postMessage')
    def test_event_message_deleted(self, mock_postMessage):
        rv = self.app.post('/slack/events/subscription',
                           json={'api_app_id': 'AL5C6CLDU',
                                 'authed_users': ['UL2PQ574L'],
                                 'event': {'channel': 'C350CNL31',
                                           'channel_type': 'channel',
                                           'deleted_ts': '1562112410.001401',
                                           'event_ts': '1562112412.001900',
                                           'hidden': True,
                                           'subtype': 'message_deleted',
                                           'ts': '',
                                           'type': 'message'},
                                 'event_id': 'EvL2Q9L412',
                                 'event_time': 1562112412,
                                 'team_id': 'T33J7GWFJ',
                                 'token': '3rm7Ngf57te4ncHKwSvWhseb',
                                 'type': 'event_callback'})
        self.assertEqual(200, rv.status_code)

    @patch('slack_resurrect.main.SLACK_CLIENT.chat_postMessage')
    def test_remove_from_channel(self, mock_postMessage):
        rv = self.app.post('/slack/events/subscription',
                           json={'api_app_id': 'AL5C6CLDU',
                                 'authed_users': ['UL2PQ574L'],
                                 'event': {'channel': 'DL385UKS4',
                                           'channel_type': 'im',
                                           'event_ts': '1562112298.000100',
                                           'team': 'T33J7GWFJ',
                                           'text': 'You have been removed from #reliability by <@U350CNF47>',
                                           'ts': '1562112298.000100',
                                           'type': 'message',
                                           'user': 'USLACKBOT'},
                                 'event_id': 'EvL390GQ93',
                                 'event_time': 1562112298,
                                 'team_id': 'T33J7GWFJ',
                                 'token': '3rm7Ngf57te4ncHKwSvWhseb',
                                 'type': 'event_callback'})
        self.assertEqual(200, rv.status_code)

    @patch('slack_resurrect.main.SLACK_CLIENT.chat_postMessage')
    def test_user_has_joiend(self, mock_postMessage):
        rv = self.app.post('/slack/events/subscription',
                           json={'api_app_id': 'AL5C6CLDU',
                                 'authed_users': ['UL2PQ574L'],
                                 'event': {'channel': 'C5S3A5WJV',
                                           'channel_type': 'channel',
                                           'event_ts': '1562112257.000200',
                                           'inviter': 'U350CNF47',
                                           'subtype': 'channel_join',
                                           'text': '<@UL2PQ574L> has joined the channel',
                                           'ts': '1562112257.000200',
                                           'type': 'message',
                                           'user': 'UL2PQ574L'},
                                 'event_id': 'EvL54AAX7H',
                                 'event_time': 1562112257,
                                 'team_id': 'T33J7GWFJ',
                                 'token': '3rm7Ngf57te4ncHKwSvWhseb',
                                 'type': 'event_callback'})
        self.assertEqual(200, rv.status_code)

    @patch('slack_resurrect.main.SLACK_CLIENT.chat_postMessage')
    def test_message_deleted(self, mock_postMessage):
        rv = self.app.post('/slack/events/subscription',
                           json={'api_app_id': 'AL5C6CLDU',
                                 'authed_users': ['UL2PQ574L'],
                                 'event': {'channel': 'C350CNL31',
                                           'channel_type': 'channel',
                                           'deleted_ts': '1562112410.001401',
                                           'event_ts': '1562112412.001900',
                                           'hidden': True,
                                           'subtype': 'message_deleted',
                                           'ts': '',
                                           'type': 'message'},
                                 'event_id': 'EvL2Q9L412',
                                 'event_time': 1562112412,
                                 'team_id': 'T33J7GWFJ',
                                 'token': '3rm7Ngf57te4ncHKwSvWhseb',
                                 'type': 'event_callback'})
        self.assertEqual(200, rv.status_code)

    @patch('slack_resurrect.main.SLACK_CLIENT.chat_postMessage')
    def test_legit_message(self, mock_postMessage):
        rv = self.app.post('/slack/events/subscription',
                           json={'api_app_id': 'AL5C6CLDU',
                                 'authed_users': ['UL2PQ574L'],
                                 'event': {'channel': 'C350CNL31',
                                           'channel_type': 'channel',
                                           'client_msg_id': 'daa756b6-0eba-4661-89fd-d093ce0dabce',
                                           'event_ts': '1562113558.002100',
                                           'team': 'T33J7GWFJ',
                                           'text': 'wazzup',
                                           'ts': '1562113558.002100',
                                           'type': 'message',
                                           'user': 'U350CNF47'},
                                 'event_id': 'EvKRS8QG1G',
                                 'event_time': 1562113558,
                                 'team_id': 'T33J7GWFJ',
                                 'token': '3rm7Ngf57te4ncHKwSvWhseb',
                                 'type': 'event_callback'})
        self.assertEqual(200, rv.status_code)

    @patch('slack_resurrect.main.SLACK_CLIENT.chat_postMessage')
    def test_lookup_user(self, mock_postMessage):
        rv = self.app.post('/slack/events/subscription',
                           json={'api_app_id': 'AL5C6CLDU',
                                 'authed_users': ['UL2PQ574L'],
                                 'event': {'channel': 'C350CNL31',
                                           'client_msg_id': '10c6beee-ba29-49ca-9cea-55ba15b7b765',
                                           'event_ts': '1562113670.002300',
                                           'team': 'T33J7GWFJ',
                                           'text': '<@UL2PQ574L> gavin',
                                           'ts': '1562113670.002300',
                                           'type': 'app_mention',
                                           'user': 'U350CNF47'},
                                 'event_id': 'EvL2QM63RA',
                                 'event_time': 1562113670,
                                 'team_id': 'T33J7GWFJ',
                                 'token': '3rm7Ngf57te4ncHKwSvWhseb',
                                 'type': 'event_callback'})
                           # json={'api_app_id': 'AL5C6CLDU',
                           #       'authed_users': ['UL2PQ574L'],
                           #       'event': {'channel': 'C350CNL31',
                           #                 'channel_type': 'channel',
                           #                 'client_msg_id': '10c6beee-ba29-49ca-9cea-55ba15b7b765',
                           #                 'event_ts': '1562113670.002300',
                           #                 'team': 'T33J7GWFJ',
                           #                 'text': '<@UL2PQ574L> gavin',
                           #                 'ts': '1562113670.002300',
                           #                 'type': 'message',
                           #                 'user': 'U350CNF47'},
                           #       'event_id': 'EvKRS9QP8A',
                           #       'event_time': 1562113670,
                           #       'team_id': 'T33J7GWFJ',
                           #       'token': '3rm7Ngf57te4ncHKwSvWhseb',
                           #       'type': 'event_callback'})
        self.assertEqual(200, rv.status_code)
        self.assertEqual(mock_postMessage.call_count, 1)
        mock_postMessage.assert_called_once_with(
            channel='C350CNL31',
            text='*Gavin Mogan:* wazzup'
        )
