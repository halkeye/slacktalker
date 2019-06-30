# About

A fun little slack app to resurrect past people using "AI"

Originally written by Callum Stsyan and Dan Ellis - https://github.com/saucelabs/slacktalker

## Configuration

Configuration is done by environment variables

* SLACK_BOT_TOKEN - OAuth Access Token
* DATABASE_URL - SQLAlchemy database uris - https://docs.sqlalchemy.org/en/13/core/engines.html#database-urls<Paste>
 * Mysql example: mysql://root@localhost/slackresurrect?charset=utf8
 * Postgres example: postgresql://postgres:@localhost/slackresurrect
* ROLLBAR_TOKEN - optional - Token to talk to rollbar

## Installation

1) Create a slack app - https://api.slack.com/apps
2) Navigate to the "OAuth & Permissions" sub screen
3) Grab the "Bot User OAuth Access Token" and populate the "SLACK_BOT_TOKEN" configuration variable
4) Make sure bots scope is added to permission scopes
5) Create a database
6) Populate the "DATABASE_URL" variable

## Importing Existing Data

1) Export data from slack - See https://get.slack.help/hc/en-us/articles/201658943-Exporting-your-team-s-Slack-history
2) Copy zip to where code is
3) Run `python import.py $zipfile`
4) Celebrate the success


