import requests
from bs4 import BeautifulSoup


def parse_oxford(word):
    TEMPLATE_URL = 'https://www.oxfordlearnersdictionaries.com/us/definition/american_english/'
    HEADERS = {'User-Agent': 'Mozilla/5.0'}
    request = TEMPLATE_URL + word
    response = requests.get(request, headers=HEADERS)
    html = BeautifulSoup(response.text, 'html.parser')
    definitions = html.find_all('span', 'def')
    if len(definitions) == 0:
        return False
    definitions = [definition.contents for definition in definitions]
    definitions_clear = []
    for definition in definitions:
        definition_clear = []
        for elem in definition:
            if '<' not in str(elem):
                definition_clear.append(str(elem))
            else:
                definition_clear.append(elem.contents[0])
        definitions_clear.append(''.join(definition_clear))
    return definitions_clear
