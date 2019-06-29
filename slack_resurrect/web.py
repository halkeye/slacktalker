import os

import rollbar
import logging
from flask import Flask, render_template
from werkzeug.contrib.fixers import ProxyFix
from healthcheck import HealthCheck, EnvironmentDump
from .model import get_engine

LOG = logging.getLogger(__name__)

app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), 'templates'),
    static_url_path=os.path.join(os.path.dirname(__file__), 'static')
)
app.wsgi_app = ProxyFix(app.wsgi_app)
health = HealthCheck(app, "/healthcheck")


# add your own check function to the healthcheck
def db_available():
    engine = get_engine()
    try: 
        result = engine.execute("SELECT 1")
        result.close()
        return True, "db ok"
    except:
        LOG.error("Exception occurred", exc_info=True)
        rollbar.report_exc_info()
        return False, "db failure"


health.add_check(db_available)


# add your own data to the environment dump
def application_data():
    return {"maintainer": "Frank Stratton",
            "git_repo": "https://github.com/Runscope/healthcheck"}


@app.route('/')
def hello_world():
    return 'Hello, World!'


@app.route('/tmpl')
def test_tmpl():
    return render_template(
        'moo.html',
        data=dict()
    )
