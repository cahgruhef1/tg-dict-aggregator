import telebot
from parse_dicts import *


class Word():

    def __init__(self, word: str,
                       defs: list = None,
                       synonyms: list = None,
                       antonyms: list = None,
                       examples: list = None):
        self.word = word
        self.defs = [] if defs is None else defs
        self.synonyms = [] if synonyms is None else synonyms
        self.antonyms = [] if antonyms is None else antonyms
        self.examples = [] if examples is None else examples

    def get_defs(self):
        for parse_func in [parse_dictionary_com,
                           parse_merriam_webster,
                           parse_oxford,
                           parse_wiktionary]:
            try:
                self.defs.append(parse_func(self.word))
            except KeyError:
                continue


bot = telebot.TeleBot("7933991416:AAGofZGQVe9Gl7GYVkvUaqH0OBS1X6TV6v4", parse_mode="HTML")
users = {}

@bot.message_handler(commands=["start"])
def start(message):
	bot.reply_to(message, "Hi there! This is Telegram Dictionary Aggregator – a bot that compiles information about words from online dictionaries in a user-friendly way. Type “/help” for a list of all commands.")

@bot.message_handler(commands=["help"])
def get_help(message):
    bot.reply_to(message, """Here is a list of the available commands:
1) /start – start the bot,
2) /help – get a list of all available commands,
3) /get_word – get the definition of a word from different dictionaries.""")

@bot.message_handler(commands=["get_word"])
def get_word(message):
    bot.reply_to(message , "Enter a word to get its definitions:")
    if message.chat.id not in users:
        users[message.chat.id] = {}
    bot.register_next_step_handler(message, get_word2)

def get_word2(message):
    w = message.text
    users[message.chat.id].update({w: Word(w)})
    users[message.chat.id][w].get_defs()
    bot.reply_to(message, f"""Here is a list of all definitions:
{"\n— ".join(users[message.chat.id][w].defs)}""")

@bot.message_handler(func=lambda message: True)
def send_default_reply(message):
	bot.reply_to(message, "Sorry, I don’t understand. Type “/help” for a list of all commands.")


bot.infinity_polling()

