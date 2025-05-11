import re
import requests
from bs4 import BeautifulSoup


def parse_dictionary_com(word: str):
    TEMPLATE_URL = 'https://www.dictionary.com/browse/'
    request_url = TEMPLATE_URL + word.lower()
    response = requests.get(request_url)
    bs = BeautifulSoup(response.text, "html.parser")
    definitions = bs.find_all('div', 'NZKOFkdkcvYgD3lqOIJw')
    if len(definitions) != 0:
        definition = definitions[0].text.split('<!-- -->')[0]
        return definition
    raise KeyError("Word not found.")

def parse_merriam_webster(word: str):
    TEMPLATE_URL = "https://www.merriam-webster.com/dictionary/"
    request_url = TEMPLATE_URL + word.lower()
    response = requests.get(request_url)
    bs = BeautifulSoup(response.text, "html.parser")
    definition = bs.find_all("span", "dtText")
    definitions = [re.sub(": ", "", elem.text) for elem in definition]
    if len(definitions) != 0:
        return "; ".join(definitions)
    raise KeyError("Word not found.")

def parse_oxford(word: str):
    TEMPLATE_URL = "https://www.oxfordlearnersdictionaries.com/us/definition/american_english/"
    HEADERS = {'User-Agent': 'Mozilla/5.0'}
    request = TEMPLATE_URL + word.lower()
    response = requests.get(request, headers=HEADERS)
    html = BeautifulSoup(response.text, "html.parser")
    definitions = html.find_all("span", "def")
    if len(definitions) == 0:
        raise KeyError("Word not found.")
    definitions = [definition.contents for definition in definitions]
    definitions_clear = []
    for definition in definitions:
        definition_clear = []
        for elem in definition:
            if '<' not in str(elem):
                definition_clear.append(str(elem))
            else:
                definition_clear.append(elem.contents[0])
        definitions_clear.append("".join(definition_clear))
    return "; ".join(definitions_clear)

def parse_wiktionary(word: str):
    REQUEST_TEMPLATE = 'https://api.dictionaryapi.dev/api/v2/entries/en/'
    result = eval(requests.get(REQUEST_TEMPLATE + word).text)
    try:
        definition = result[0]['meanings'][0]['definitions'][0]['definition']
    except KeyError:
        raise KeyError("Word not found.")
    return definition

if __name__ == "__main__":
    word = input()
    print(parse_dictionary_com(word))
    print(parse_merriam_webster(word))
    print(parse_oxford(word))
    print(parse_wiktionary(word))

