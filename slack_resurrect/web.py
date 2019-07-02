import os
import logging

import sentry_sdk
from flask import Flask, render_template, request
from sentry_sdk.integrations.flask import FlaskIntegration
from werkzeug.contrib.fixers import ProxyFix
from healthcheck import HealthCheck
from .model import get_engine
from .main import CONFIG, parse_direct_mention, handle_command, save_user, save_message

LOG = logging.getLogger(__name__)

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
    static_url_path=''
)
app.wsgi_app = ProxyFix(app.wsgi_app)
app.health = HealthCheck(app, "/healthcheck")

if CONFIG.SENTRY_TOKEN:
    sentry_sdk.init(
        CONFIG.SENTRY_TOKEN,
        environment=CONFIG.SENTRY_ENVIRONMENT,
        integrations=[FlaskIntegration()]
    )


# add your own check function to the healthcheck
def db_available():
    engine = get_engine()
    try: 
        result = engine.execute("SELECT 1")
        result.close()
        return True, "db ok"
    except Exception as exp:
        LOG.error("Exception occurred", exc_info=True)
        sentry_sdk.capture_exception(exp)
        return False, "db failure"


app.health.add_check(db_available)


@app.route('/')
def root():
    return render_template(
        'index.html',
        data=dict()
    )


@app.route('/slack/events/subscription', methods=['GET', 'POST'])
def subscription():
    slack_event = request.json
    if slack_event['token'] != CONFIG.SLACK_TOKEN:
        return 403

    if slack_event['type'] == 'url_verification':
        return slack_event['challenge']

    if slack_event['type'] == 'event_callback':
        event = slack_event['event']
        if event['type'] == 'app_mention':
            user_id, message = parse_direct_mention(event["text"])
            if message:
                handle_command(message, event["channel"])
        if event['type'] == 'message':
            user_id, message = parse_direct_mention(event["text"])
            if not message:
                save_user(event)
                save_message(event)

    if CONFIG.DEBUG:
        from pprint import pprint
        pprint(slack_event)

    return ''
