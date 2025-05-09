import requests


def parse_wiktionary(word: str):
    REQUEST_TEMPLATE = 'https://api.dictionaryapi.dev/api/v2/entries/en/'
    result = eval(requests.get(REQUEST_TEMPLATE + word).text)
    try:
        definition = result[0]['meanings'][0]['definitions'][0]['definition']
    except KeyError:
        return "Word not found."
    return definition


if __name__ == "__main__":
    print(parse_wiktionary(input()))

