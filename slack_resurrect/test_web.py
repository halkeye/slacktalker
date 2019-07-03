# pylint: disable=redefined-outer-name
import pytest
from .main import SLACK_CLIENT
from .web import create_app
from .db import db


def monkeypatch_return_postMessage(*args, **kwargs):
    return {'ok': True}


@pytest.yield_fixture(scope='function')
def client():
    app = create_app()
    test_app = app.test_client()
    test_app.debug = True
    with app.app_context():
        db.create_all()

    yield test_app

    with app.app_context():
        # Explicitly close DB connection
        db.session.close()

        db.drop_all()


def resource_user_json():
    return dict(
        user={
            "id": "U0GEMHWDP",
            "team_id": "T02QDM2DV",
            "name": "halkeye",
            "deleted": False,
            "color": "9d8eee",
            "real_name": "Gavin Mogan",
            "tz": "America/Los_Angeles",
            "tz_label": "Pacific Daylight Time",
            "tz_offset": -25200,
            "profile": {
                "title": "Code Monkey",
                "phone": "(406) 838-6832",
                "skype": "",
                "real_name": "Gavin Mogan",
                "real_name_normalized": "Gavin Mogan",
                "display_name": "halkeye",
                "display_name_normalized": "halkeye",
                "fields": [],
                "status_text": "",
                "status_emoji": "",
                "status_expiration": 0,
                "avatar_hash": "54927104a919",
                "image_original": "https://avatars.slack-edge.com/2018-11-18/482696063474_54927104a9199fc3df69_original.jpg",
                "email": "fake@email",
                "first_name": "Gavin",
                "last_name": "Mogan",
                "image_24": "https://avatars.slack-edge.com/2018-11-18/482696063474_54927104a9199fc3df69_24.jpg",
                "image_32": "https://avatars.slack-edge.com/2018-11-18/482696063474_54927104a9199fc3df69_32.jpg",
                "image_48": "https://avatars.slack-edge.com/2018-11-18/482696063474_54927104a9199fc3df69_48.jpg",
                "image_72": "https://avatars.slack-edge.com/2018-11-18/482696063474_54927104a9199fc3df69_72.jpg",
                "image_192": "https://avatars.slack-edge.com/2018-11-18/482696063474_54927104a9199fc3df69_192.jpg",
                "image_512": "https://avatars.slack-edge.com/2018-11-18/482696063474_54927104a9199fc3df69_512.jpg",
                "image_1024": "https://avatars.slack-edge.com/2018-11-18/482696063474_54927104a9199fc3df69_1024.jpg",
                "status_text_canonical": "",
                "team": "T02QDM2DV",
                "is_custom_image": True
            },
            "is_admin": False,
            "is_owner": False,
            "is_primary_owner": False,
            "is_restricted": False,
            "is_ultra_restricted": False,
            "is_bot": False,
            "is_app_user": False,
            "updated": 1561695650
        }
    )


def test_root(client):
    print(client)
    rv = client.get('/')
    assert rv.status_code == 200


def test_event_message_deleted(client, monkeypatch):
    monkeypatch.setattr(SLACK_CLIENT, "chat_postMessage", monkeypatch_return_postMessage)
    monkeypatch.setattr(SLACK_CLIENT, "users_info", lambda user: resource_user_json())
    rv = client.post('/slack/events/subscription',
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
    assert rv.status_code == 200


def test_remove_from_channel(client, monkeypatch):
    monkeypatch.setattr(SLACK_CLIENT, "chat_postMessage", monkeypatch_return_postMessage)
    monkeypatch.setattr(SLACK_CLIENT, "users_info", lambda user: resource_user_json())
    rv = client.post('/slack/events/subscription',
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
    assert rv.status_code == 200


def test_user_has_joiend(client, monkeypatch):
    monkeypatch.setattr(SLACK_CLIENT, "chat_postMessage", monkeypatch_return_postMessage)
    monkeypatch.setattr(SLACK_CLIENT, "users_info", lambda user: resource_user_json())
    rv = client.post('/slack/events/subscription',
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
    assert rv.status_code == 200


def test_message_deleted(client, monkeypatch):
    monkeypatch.setattr(SLACK_CLIENT, "chat_postMessage", monkeypatch_return_postMessage)
    monkeypatch.setattr(SLACK_CLIENT, "users_info", lambda user: resource_user_json())
    rv = client.post('/slack/events/subscription',
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
    assert rv.status_code == 200


def test_legit_message(client, monkeypatch):
    monkeypatch.setattr(SLACK_CLIENT, "chat_postMessage", monkeypatch_return_postMessage)
    monkeypatch.setattr(SLACK_CLIENT, "users_info", lambda user: resource_user_json())
    rv = client.post('/slack/events/subscription',
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
    assert rv.status_code == 200


def test_lookup_user(client, monkeypatch, mocker):
    mock_chat_postMessage = mocker.Mock()
    mock_chat_postMessage.return_value = monkeypatch_return_postMessage()
    monkeypatch.setattr(SLACK_CLIENT, "chat_postMessage", mock_chat_postMessage)
    monkeypatch.setattr(SLACK_CLIENT, "users_info", lambda user: resource_user_json())
    rv = client.post('/slack/events/subscription',
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
    assert rv.status_code == 200
    assert mock_chat_postMessage.call_count == 1
    mock_chat_postMessage.assert_called_once_with(
        channel='C350CNL31',
        text='Username "gavin" not found'
    )
