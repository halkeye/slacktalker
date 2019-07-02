import time
import logging

import sentry_sdk

from slack import RTMClient
from slack_resurrect.main import SLACK_CLIENT, RTM_READ_DELAY, set_bot_id, parse_message_event
from slack_resurrect.model import create_all
from slack_resurrect.settings import CONFIG
from slack_resurrect.web import app

LOG = logging.getLogger(__name__)

if CONFIG.SENTRY_TOKEN:
    sentry_sdk.init(CONFIG.SENTRY_TOKEN, environment=CONFIG.SENTRY_ENVIRONMENT)

try:
    create_all()
except Exception as exp:
    LOG.error("Exception occurred", exc_info=True)
    sentry_sdk.capture_exception(exp)
    raise SystemExit()


rtmclient = RTMClient(token=CONFIG.SLACK_BOT_TOKEN)


@RTMClient.run_on(event='open')
def startup(**payload):
    set_bot_id(SLACK_CLIENT.auth_test()["user_id"])
    print("Starter Bot connected and running!")


@RTMClient.run_on(event='message')
def say_hello(**payload):
    print(payload)
    event = payload['data']
    if 'subtype' in event:
        return
    try:
        event['type'] = 'message'
        parse_message_event(event)
    except Exception as exp:
        LOG.error("Exception occurred", exc_info=True)
        sentry_sdk.capture_exception(exp)

rtmclient.start()
