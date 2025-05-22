import telebot
from parse_dicts import *
from get_word_of_the_day import *
from generate_image import *
import time


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

    def get_defs(self, dictionaries=[parse_dictionary_com, parse_merriam_webster, parse_oxford, parse_collins, parse_vocabulary]):
        for parse_func in dictionaries:
            try:
                self.defs.append(parse_func(self.word))
            except KeyError:
                continue
    def get_synonyms(self):
        self.synonyms.extend(parse_synonyms_collins(self.word))
    def get_examples(self):
        try:
            self.examples.extend(parse_examples_collins(self.word))
        except KeyError:
            pass


bot = telebot.TeleBot("", parse_mode="HTML")
users = {}

dict_list = ["1. meriam-webster.com", "2. dictionary.com", "3. Oxford Learner's dictionary", "4. vocabulary.com", "5. Collins dictionary"]
dict_list = "\n".join(dict_list)
dict_func_dict = {"1": parse_merriam_webster, "2": parse_dictionary_com, "3": parse_oxford, "4": parse_vocabulary, "5": parse_collins}


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
    users[message.chat.id].setdefault("selected_dictionaries", [parse_dictionary_com, parse_merriam_webster, parse_oxford, parse_collins, parse_vocabulary])
    users[message.chat.id][w].get_defs(users[message.chat.id]["selected_dictionaries"])
    users[message.chat.id][w].get_synonyms()
    users[message.chat.id][w].get_examples()
    if users[message.chat.id][w].defs == []:
        bot.reply_to(message, "I don’t know this word. Enter another word.")
    else:
        parts_of_message = []
        defs_joined = "\n— ".join(users[message.chat.id][w].defs)
        defs_message  = f"""Here is a list of all definitions: \n—
{defs_joined}"""
        parts_of_message.append(defs_message)
        if len(users[message.chat.id][w].synonyms) != 0:
            synonyms_joined = "\n—".join(users[message.chat.id][w].synonyms)
            synonyms_message = f"Here are synonyms to your word: \n—{synonyms_joined}"
            parts_of_message.append(synonyms_message)
        if len(users[message.chat.id][w].examples) != 0:
            examples_joined = "\n—".join(users[message.chat.id][w].examples)
            examples_message = f"Here are examples with your word: \n—{examples_joined}"
            parts_of_message.append(examples_message)
        bot.reply_to(message, "\n\n".join(parts_of_message))
	    generate_image_with_text(w, get_vocabulary_info(w), f"./{w}.png")
        bot.send_photo(message.chat.id, photo=open(f"./{w}.png", "rb"))


@bot.message_handler(commands=["subscribe_to_word_of_the_day"])
def get_level(message):
    bot.send_message(message.chat.id, "Select a vocabulary level: a1, a2, b1, b2, c1")
    if message.chat.id not in users:
        users[message.chat.id] = {}
    bot.register_next_step_handler(message, start_subscription)


def start_subscription(message):
    level = message.text
    users[message.chat.id].setdefault("subscription", {"levels": [], "subscription_status": True, "word_of_the_day_id": 1})
    users[message.chat.id]["subscription"]["levels"].append(level)
    while users[message.chat.id]["subscription"]["subscription_status"]:
        for level in users[message.chat.id]["subscription"]["levels"]:
            word_of_the_day = get_word_of_the_day(users[message.chat.id]["subscription"]["word_of_the_day_id"], level)
            users[message.chat.id].update({word_of_the_day: Word(word_of_the_day)})
            users[message.chat.id][word_of_the_day].get_defs()
            defs_joined = "\n— ".join(users[message.chat.id][word_of_the_day].defs)
            bot.send_message(message.chat.id, f"""Here is a list of all definitions for {word_of_the_day}:
            {defs_joined}""")
            users[message.chat.id]["subscription"]["word_of_the_day_id"] += 1
            generate_image_with_text(word_of_the_day, get_vocabulary_info(word_of_the_day), f"./{word_of_the_day}.png")
            bot.send_photo(message.chat.id, photo=open(f"./{word_of_the_day}.png", "rb"))
            time.sleep(86400)


@bot.message_handler(commands=["unsubscribe_from_word_of_the_day"])
def unsubscribe(message):
    users[message.chat.id]["subscription"]["subscription_status"] = False
    bot.send_message(message.chat.id, "You have unsubscribed from word of the day.")
    bot.register_next_step_handler(message, start_subscription)


@bot.message_handler(commands=["select_dicts"])
def send_choice(message):
    bot.send_message(message.chat.id, f"Please select definitions from which dictionaries you want to get:\n {dict_list}\n "
                                      f"Write a list of numbers separated by a comma")
    bot.register_next_step_handler(message, select_dicts)


def select_dicts(message):
    selected_numbers = message.text.split(",")
    selected_functions = [dict_func_dict[number.strip()] for number in selected_numbers]
    users[message.chat.id]["selected_dictionaries"] = selected_functions


@bot.message_handler(func=lambda message: True)
def send_default_reply(message):
	bot.reply_to(message, "Sorry, I don’t understand. Type “/help” for a list of all commands.")


bot.infinity_polling()

