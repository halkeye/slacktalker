"""
Slack glue to the resurrect modules
"""
import re
import logging
from slack import WebClient
from .model import User, WordEntry
from .db import db
from .talker_exceptions import TalkerException
from .make_sentence import make_sentence
from .settings import CONFIG

LOG = logging.getLogger(__name__)
# instantiate Slack client
SLACK_CLIENT = WebClient(token=CONFIG.SLACK_BOT_TOKEN)
# starterbot's user ID in Slack: value is assigned after the bot starts up
BOT_ID = None

# constants
RTM_READ_DELAY = 1  # 1 second delay between reading from RTM
MENTION_REGEX = "^<@(|[WU].+?)>(.*)"


def set_bot_id(_id):
    """
    Sets the global bot id
    """
    global BOT_ID  # pylint: disable=global-statement
    BOT_ID = _id


def save_user(item):
    """
    {
        "type": "message",
        "user": "U02FVR4ND",
        "text": "isaac: we're heading to dinner around 7pm",
        "ts": "1409746135.000671"
    }
    """
    # Only messages
    if item['type'] != 'message':
        return
    # Skip bots
    if 'bot_id' in item:
        return
    # Ignore edits
    if 'subtype' in item:
        return
    return save_actual_user(item['user'])


def save_actual_user(userId):
    db_user = User.byid(db.session, userId)

    if not db_user:
        slack_user = SLACK_CLIENT.users_info(user=userId).get('user')
        db_user = User.new_from_slack(slack_user)
        db.session.add(db_user)

    db.session.commit()
    return db_user


def save_message(item):
    """
    {
        "type": "message",
        "user": "U02FVR4ND",
        "text": "isaac: we're heading to dinner around 7pm",
        "ts": "1409746135.000671"
    }
    """
    # Only messages
    if item['type'] != 'message':
        return
    # Skip bots
    if 'bot_id' in item:
        return
    # Ignore edits
    if 'subtype' in item:
        return
    words = item['text'].split()
    for i in list(range(len(words) + 1)):
        user = item['user']
        word_prev = words[i - 1].lower()[:254] if i > 0 else ''
        word_next = words[i].lower()[:254] if i < len(words) else ''
        word_entry = db.session.query(WordEntry).filter(
            WordEntry.user == user,
            WordEntry.word_prev == word_prev,
            WordEntry.word_next == word_next
        ).first()
        if not word_entry:
            word_entry = WordEntry()
            word_entry.user = user
            word_entry.word_prev = word_prev
            word_entry.word_next = word_next
            word_entry.count = 0
        word_entry.count += 1
        db.session.add(word_entry)

    #two word combos
    for i, word_next in enumerate(words):
        word_next = word_next.lower()[:254]
        if i < 2:
            continue
        word_prev = '%s %s' % (
            words[i - 2].lower()[:254],
            words[i - 1].lower()[:254]
        )
        word_entry = db.session.query(WordEntry).filter(
            WordEntry.user == user,
            WordEntry.word_prev == word_prev,
            WordEntry.word_next == word_next
        ).first()
        if not word_entry:
            word_entry = WordEntry()
            word_entry.user = user
            word_entry.word_prev = word_prev
            word_entry.word_next = word_next
            word_entry.count = 0
        word_entry.count += 1

        db.session.add(word_entry)

    db.session.commit()


def parse_message_event(event):
    """
    Given a slack event, parse out the bot command, then respond if nesessary
    or save to the db
    """
    user_id, message = parse_direct_mention(event["text"])
    if BOT_ID and user_id == BOT_ID:
        handle_command(event["team_id"], message, event["channel"])
    else:
        save_user(event)
        save_message(event)


def parse_direct_mention(message_text):
    """
    Finds a direct mention (a mention that is at the beginning) in message text
    and returns the user ID which was mentioned.
    If there is no direct mention, returns None
    """
    matches = re.search(MENTION_REGEX, message_text)

    # the first group contains the username
    # the second group contains the remaining message
    if matches:
        return (matches.group(1), matches.group(2).strip())

    return (None, None)


def handle_command(team_id, command, channel):
    """
    Executes bot command if the command is known
    """
    # Default response is help text for the user
    default_response = "Not sure what you mean"

    # Finds and executes the given command, filling in response
    response = None

    (username, prompt) = (command + " ").split(" ", 1)
    if username:
        try:
            response = make_sentence(team_id, username, prompt)
        except TalkerException as err:
            response = str(err)

    # Sends the response back to the channel
    SLACK_CLIENT.chat_postMessage(
        channel=channel,
        text=response or default_response
    )
    return ""
