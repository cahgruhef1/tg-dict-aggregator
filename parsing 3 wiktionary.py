import requests


def parse_wiktionary_definition(word: str):
    REQUEST_TEMPLATE = 'https://api.dictionaryapi.dev/api/v2/entries/en/'
    result = eval(requests.get(REQUEST_TEMPLATE + word).text)
    definition = result[0]['meanings'][0]['definitions'][0]['definition']
    return definition
