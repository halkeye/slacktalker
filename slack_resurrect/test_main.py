import pytest
from .main import (
    set_bot_id,
    parse_direct_mention
)
from .model import (
    User
)


@pytest.yield_fixture(autouse=True)
def run_around_tests():
    set_bot_id('U123BOT')


def test_parse_direct_mention():
    assert parse_direct_mention("<@U123BOT> gavin") == ("U123BOT", "gavin")
    assert parse_direct_mention("isaac: we're heading to dinner around 7pm") == (None, None)


def test_save_user():
    slack_user = {
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
    db_user = User.new_from_slack(slack_user)
    assert db_user.team_id == 'T02QDM2DV'
    assert db_user.id == 'U0GEMHWDP'
    assert db_user.pretty_name == 'Gavin Mogan'
