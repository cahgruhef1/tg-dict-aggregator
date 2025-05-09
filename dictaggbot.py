import telebot

bot = telebot.TeleBot("7933991416:AAGofZGQVe9Gl7GYVkvUaqH0OBS1X6TV6v4", parse_mode="HTML") # You can set parse_mode by default. HTML or MARKDOWN

@bot.message_handler(commands=["start"])
def start(message):
	bot.send_message(message, "Hi there! This is Telegram Dictionary Aggregator – a bot that compiles information about words from online dictionaries in a user-friendly way. Type “/help” for a list of all commands.")

@bot.message_handler(commands=["help"])
def get_help(message):
    bot.send_message(message, """Here is a list of the available commands:
1) /start – start the bot,
2) /help – get a list of all available commands.""")

@bot.message_handler(func=lambda message: True)
def send_default_reply(message):
	bot.send_message(message, "Sorry, I don’t understand. Type “/help” for a list of all commands.")

bot.infinity_polling()

