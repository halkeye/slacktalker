import os
import logging

import sentry_sdk
from flask import Flask, render_template, request
from werkzeug.middleware.proxy_fix import ProxyFix
from healthcheck import HealthCheck
from .db import db
from .main import CONFIG, parse_direct_mention, handle_command, save_user, save_message


def create_app():
    LOG = logging.getLogger(__name__)
    app = Flask(
        __name__,
        template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
        static_url_path=''
    )

    app.config.from_object(CONFIG)
    app.wsgi_app = ProxyFix(app.wsgi_app)
    app.health = HealthCheck(app, "/healthcheck")
    db.init_app(app)

    # add your own check function to the healthcheck
    def db_available():
        try:
            result = db.engine.execute("SELECT 1")
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
            return ('', 403)

        if slack_event['type'] == 'url_verification':
            return slack_event['challenge']

        if CONFIG.DEBUG:
            from pprint import pprint
            pprint(slack_event)

        if slack_event['type'] == 'event_callback':
            event = slack_event['event']
            if 'subtype' in event:
                return ''

            if event['type'] == 'app_mention':
                user_id, message = parse_direct_mention(event["text"])
                if message:
                    handle_command(slack_event['team_id'], message, event["channel"])
            if event['type'] == 'message':
                user_id, message = parse_direct_mention(event["text"])
                if not message:
                    save_user(event)
                    save_message(event)

        return ''

    return app
