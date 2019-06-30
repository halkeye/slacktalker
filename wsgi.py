import logging

import rollbar

from slack_resurrect.model import create_all
from slack_resurrect.settings import CONFIG
from slack_resurrect.web import app

LOG = logging.getLogger(__name__)

rollbar.init(CONFIG.ROLLBAR_TOKEN, CONFIG.ROLLBAR_ENVIRONMENT)

try:
    create_all()
except:
    LOG.error("Exception occurred", exc_info=True)
    rollbar.report_exc_info()
    raise SystemExit()

if __name__ == '__main__':
    app.run(
        debug=CONFIG.DEBUG,
        port=int(CONFIG.PORT),
        host="0.0.0.0"
    )
