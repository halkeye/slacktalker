import pytest
from .main import set_bot_id, parse_direct_mention


@pytest.yield_fixture(autouse=True)
def run_around_tests():
    set_bot_id('U123BOT')


def test_parse_direct_mention():
    assert parse_direct_mention("<@U123BOT> gavin") == ("U123BOT", "gavin")
    assert parse_direct_mention("isaac: we're heading to dinner around 7pm") == (None, None)
