import os


class Config:
    @classmethod
    def toJSON(cls):
        import json
        data = dict()
        for item in dir(cls):
            if item.isupper():
                data[item] = getattr(cls, item)
        return json.dumps(data)

    DEBUG = False
    TESTING = False
    DEBUG_SQL = False
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SENTRY_TOKEN = os.environ.get('SENTRY_TOKEN')
    SENTRY_ENVIRONMENT = None
    SLACK_BOT_TOKEN = os.environ.get('SLACK_BOT_TOKEN')
    ## Webhooks token
    SLACK_TOKEN = os.environ.get('SLACK_TOKEN')
    PORT=3000


class DevelopmentConfig(Config):
    DEBUG = True
    DEBUG_SQL = True
    SENTRY_ENVIRONMENT = 'development'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.sqlite'


class TestingConfig(DevelopmentConfig):
    TESTING = True
    DEBUG_SQL = False
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SENTRY_TOKEN = None
    SENTRY_ENVIRONMENT = 'testing'


class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SENTRY_ENVIRONMENT = 'production'


ENV = os.environ.get('APP_ENV', os.environ.get('FLASK_ENV', 'development'))
CONFIG = None

if ENV == 'dev' or ENV == 'development':
    CONFIG = DevelopmentConfig
elif ENV == 'test':
    CONFIG = TestingConfig
elif ENV == 'prod':
    CONFIG = ProductionConfig
else:
    raise ValueError('Invalid environment name')
