from slackbot.bot import respond_to
from slackbot.bot import listen_to

NoteStore = {}

def start_taking(userid):
    NoteStore[userid] = []

def stop_taking(userid):
    notes = NoteStore.pop(userid, [])
    return "\n".join(str(note) for note in notes)

def add_note(userid, note):
    NoteStore[userid].append(note)

def get_user(message):
    return message.body['user']

def get_text(message):
    return message.body['text']

def user_is_taking_notes(userid):
    return userid in NoteStore

@respond_to('start')
def start_notes(message):
    userid = get_user(message)
    text = get_text(message)
    if user_is_taking_notes(userid):
        add_note(userid, text)
    else:
        message.reply('*Starting notes*')
        message.reply('(Type `finished` to stop taking notes)')
        start_taking(userid)

@respond_to('finished')
def finish_notes(message):
    userid = get_user(message)
    text = get_text(message)
    if user_is_taking_notes(userid):
        notes = stop_taking(userid)
        message.reply("```%s```" % notes)
    else:
        message.reply('Error. Type `start` to start taking notes')

@respond_to('(.*)')
def take_notes(message):
    userid = get_user(message)
    text = get_text(message)
    if user_is_taking_notes(userid):
        add_note(userid, text)
    else:
        message.reply('Error. Type `start` to start taking notes')