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
            db_user = User(
                id=slack_user['id'],
                name=slack_user['name'],
                real_name=slack_user['profile'].get('real_name', ''),
                first_name=slack_user['profile'].get('first_name', ''),
                last_name=slack_user['profile'].get('last_name', ''),
                image_24=slack_user['profile'].get('image_24', ''),
                image_32=slack_user['profile'].get('image_32', ''),
                image_48=slack_user['profile'].get('image_48', ''),
                image_72=slack_user['profile'].get('image_72', ''),
                image_192=slack_user['profile'].get('image_192', ''),
                image_original=slack_user['profile'].get('image_original', ''),
            )
            session.add(db_user)

    session.commit()
    for item in archive.infolist():
        if not item.is_dir() and '/' in item.filename:
            for event in json.loads(archive.read(item.filename)):
                save_message(event)


for item in sys.argv[1:]:
    main(item)
