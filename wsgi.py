import logging

import sentry_sdk

from slack_resurrect.settings import CONFIG
from slack_resurrect.web import create_app, sentry_integrations
from slack_resurrect.db import db

LOG = logging.getLogger(__name__)

if CONFIG.SENTRY_TOKEN:
    sentry_sdk.init(
        dsn=CONFIG.SENTRY_TOKEN,
        environment=CONFIG.SENTRY_ENVIRONMENT,
        integrations=sentry_integrations()
    )


app = create_app()
try:
    with app.app_context():
        db.create_all()
except Exception as exp:
    LOG.error("Exception occurred", exc_info=True)
    sentry_sdk.capture_exception(exp)
    raise SystemExit()

if __name__ == '__main__':
    app.run(
        debug=CONFIG.DEBUG,
        port=int(CONFIG.PORT),
        host="0.0.0.0"
    )
