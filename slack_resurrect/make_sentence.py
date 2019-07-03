from builtins import str, range
import random
import re

from sqlalchemy import desc, func

from .db import db
from .model import WordEntry, User
from .talker_exceptions import UserNotFoundException, UserHasntSpoken

# for each possible next word sampled from the crowd
# generate PERSONALITY_WEIGHT entries from the actual user
WORD_PAIRS_WEIGHT = 1
SENTENCE_WORD_LIMIT = 100


def get_next_word(user, word, last_words):
    user_words = db.session.query(WordEntry).filter(
        WordEntry.user == user.id, WordEntry.word_prev == word
    ).order_by(desc(WordEntry.count)).limit(10)

    user_word_pairs = db.session.query(WordEntry).filter(
        WordEntry.user == user.id, WordEntry.word_prev == last_words
    ).order_by(desc(WordEntry.count)).limit(5)

    candidates = []
    for user_word in user_words:
        candidates.append(user_word.word_next)

    for user_word in user_word_pairs:
        for _ in list(range(WORD_PAIRS_WEIGHT)):
            candidates.append(user_word.word_next)

    result = random.choice(candidates)
    return result


def make_sentence(team_id, username, prompt=""):
    sentence = ''
    # Try to find the user
    user = User.byname(db.session, team_id, username)
    if not user:
        raise UserNotFoundException(
            'Username "{}" not found'.format(username))

    sentence = ''
    word = ''
    if prompt:  # Load up an initial word
        word = db.session.query(WordEntry).filter(
            WordEntry.user == user.id,
            WordEntry.word_prev == prompt
        ).order_by(func.random()).first()
    if word:
        sentence += word.word_prev + " "
    else:
        word = db.session.query(WordEntry).filter(
            WordEntry.user == user.id,
            WordEntry.word_prev == ''
        ).order_by(func.random()).first()
    if not word:
        raise UserHasntSpoken(
            'I haven\'t seen "{}" say anything'.format(username))
    word = word.word_next
    sentence += word
    for _ in list(range(SENTENCE_WORD_LIMIT)):
        last_words = ' '.join(sentence.split()[-2:])
        word = get_next_word(user, word, last_words)
        if word:
            sentence += ' ' + word
        else:
            break
    sentence = "*{}:* {}".format(user.pretty_name, sentence)

    # Slack surrounds URLs with < and >, which breaks their linking.  So we
    # strip that out.
    sentence = re.sub(
        r'<(http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+)>',
        r'\1',
        sentence)

    # Replace @u1010101 references with actual user names
    user_ids = re.finditer(r'(@[\d\w]{9})', sentence)
    for match in user_ids:
        user_id = match.group()
        user = db.session.query(User).filter(
            User.id == user_id.strip('@')).first()
        if not user:
            continue
        sentence = sentence.replace(user_id, '@' + str(user))
    return sentence
