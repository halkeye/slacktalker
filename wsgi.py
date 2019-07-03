import logging
import sentry_sdk

from slack_resurrect.settings import CONFIG
from slack_resurrect.web import create_app, sentry_integrations
from slack_resurrect.db import db

if CONFIG.SENTRY_TOKEN:
    sentry_sdk.init(
        dsn=CONFIG.SENTRY_TOKEN,
        environment=CONFIG.SENTRY_ENVIRONMENT,
        integrations=sentry_integrations()
    )


app = None
try:
    app = create_app()

    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    app.logger.info(CONFIG.toJSON())
    with app.app_context():
        db.create_all()
    if __name__ == '__main__':
        app.run(
            debug=CONFIG.DEBUG,
            port=int(CONFIG.PORT),
            host="0.0.0.0"
        )
except Exception as exp:
    if app:
        app.logger.error("Exception occurred", exc_info=True)
    else:
        print(exp)
    sentry_sdk.capture_exception(exp)
    raise SystemExit()

