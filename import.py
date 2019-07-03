import sys
import zipfile
import json

from slack_resurrect.main import User, save_message
from slack_resurrect.db import db
from slack_resurrect.app import app


def main(filename):
    print("importing " + filename)
    archive = zipfile.ZipFile(filename, 'r')

    for slack_user in json.loads(archive.read('users.json')):
        db_user = User.byid(db.session, slack_user['id'])
        if not db_user:
            db_user = User.new_from_slack(slack_user)
            db.session.add(db_user)

    db.session.commit()
    for item in archive.infolist():
        if not item.is_dir() and '/' in item.filename:
            for event in json.loads(archive.read(item.filename)):
                save_message(event)


for item in sys.argv[1:]:
    with app.app_context():
        db.create_all()
    main(item)
