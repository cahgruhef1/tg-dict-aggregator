import telebot
from parse_dicts import *
import asyncio

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

    async def get_dictionary_com(self):
        await self.defs.append(parse_dictionary_com(self.word))
    async def get_merriam_webster(self):
        await self.defs.append(parse_merriam_webster(self.word))
    async def get_oxford(self):
        await self.defs.append(parse_oxford(self.word))
    async def get_wiktionary(self):
        await self.defs.append(parse_wiktionary(self.word))



bot = telebot.TeleBot("7933991416:AAGofZGQVe9Gl7GYVkvUaqH0OBS1X6TV6v4", parse_mode="HTML")
users = {}

@bot.message_handler(commands=["start"])
def start(message):
	bot.send_message(message.chat.id, "Hi there! This is Telegram Dictionary Aggregator – a bot that compiles information about words from online dictionaries in a user-friendly way. Type “/help” for a list of all commands.")

@bot.message_handler(commands=["help"])
def get_help(message):
    bot.send_message(message.chat.id, """Here is a list of the available commands:
1) /start – start the bot,
2) /help – get a list of all available commands,
3) /get_word – get the definition of a word from different dictionaries.""")

@bot.message_handler(commands=["get_word"])
def get_word(message):
    bot.send_message(message.chat.id, "Enter a word to get its definitions:")
    if message.chat.id not in users:
        users[message.chat.id] = {}
    bot.register_next_step_handler(message, get_word2)

def get_word2(message):
    w = message.text
    users[message.chat.id].update({w: Word(w)})
    users[message.chat.id][w].get_oxford()
    users[message.chat.id][w].get_merriam_webster()
    users[message.chat.id][w].get_dictionary_com()
    users[message.chat.id][w].get_wiktionary()
    if users[message.chat.id][w].defs == []:
        bot.reply_to(message, "I don’t know this word. Enter another word.")
    else:
        defs_joined = "\n— ".join(users[message.chat.id][w].defs)
        bot.reply_to(message, f"""Here is a list of all definitions:{defs_joined}""")

@bot.message_handler(func=lambda message: True)
def send_default_reply(message):
	bot.reply_to(message, "Sorry, I don’t understand. Type “/help” for a list of all commands.")


bot.infinity_polling()

