# Telegram Dictionary Aggregator

Telegram Dictionary Aggregator is a Telegram bot aimed at providing users with data on different vocabulary items compiled from various dictionaries. To enhance the browsing experience, the aggregated information is presented in a user-friendly way, in the form of posts with pre-generated images, example sentences, and other types of media essential for an effective learning process.

Get started by cloning this repository and trying it out for yourself!

Bot:\
@DictAggregatorBot

List of the available commands:\
1) /start – start the bot,
2) /help – get a list of all available commands,
3) /get_word – get the definition of a word from different dictionaries,
4) /subscribe_wotd - subscribe for word of the day,
5) /unsubscribe_wotd - unsubscribe from word of the day,
6) /select_dicts - choose which dictionaries to use.

Team:
Timofey Fomichev, @cahgruhef1\
Yakov Lvovsky, @jacoblvovski\
Anastasia Shvets, @AnShvts\
Irina Golikova, @Irina8820

Repository structure:
dictaggbot.py - Telegram bot framework using telebot API\
parse_dicts.py - functions for parsing different dictionaries using requests and BeautifulSoup4\
generate_image.py - Fusion Brain image generation framework

Resources:\
telebot API docs:\
https://pytba.readthedocs.io/en/latest/index.html\
https://pypi.org/project/pyTelegramBotAPI/

Fusion Brain image generation network:\
https://fusionbrain.ai/

BeatifulSoup4 parsing:\
https://beautiful-soup-4.readthedocs.io/en/latest/\
https://pypi.org/project/beautifulsoup4/

