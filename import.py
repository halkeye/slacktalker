import sys
import zipfile
import json

from slack_resurrect.main import get_session, User, save_message


def main(filename):
    print("importing " + filename)
    archive = zipfile.ZipFile(filename, 'r')

    session = get_session()
    for slack_user in json.loads(archive.read('users.json')):
        db_user = User.byid(session, slack_user['id'])
        if not db_user:
            db_user = User.new_from_slack(slack_user)
            session.add(db_user)

    session.commit()
    for item in archive.infolist():
        if not item.is_dir() and '/' in item.filename:
            for event in json.loads(archive.read(item.filename)):
                save_message(event)


for item in sys.argv[1:]:
    main(item)
