import time
import logging

import rollbar

from slack_resurrect.main import SLACK_CLIENT, RTM_READ_DELAY, set_bot_id, parse_events
from slack_resurrect.model import create_all
from slack_resurrect.settings import CONFIG

LOG = logging.getLogger(__name__)

rollbar.init(CONFIG.ROLLBAR_TOKEN)

try:
    create_all()
except:
    LOG.error("Exception occurred", exc_info=True)
    rollbar.report_exc_info()
    raise SystemExit()

if SLACK_CLIENT.rtm_connect(with_team_state=False):
    print("Starter Bot connected and running!")
    # Read bot's user ID by calling Web API method `auth.test`
    set_bot_id(SLACK_CLIENT.api_call("auth.test")["user_id"])
    while True:
        try:
            parse_events(SLACK_CLIENT.rtm_read())
        except:  # pylint: disable=broad-exception
            LOG.error("Exception occurred", exc_info=True)
            rollbar.report_exc_info()
        time.sleep(RTM_READ_DELAY)
else:
    print("Connection failed. Exception traceback printed above.")
