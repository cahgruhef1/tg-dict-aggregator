from bs4 import BeautifulSoup
import requests


def get_vocabulary_definition(word):
    url = f"https://www.vocabulary.com/dictionary/{word}"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    bs = BeautifulSoup(response.text, "html.parser")
    definitions = bs.find_all('div', class_='definition')
    definitions = [definition for definition in definitions if definition.find_all('div', class_='pos-icon')]
    definitions_clear = []
    seen_definitions = set()
    for definition in definitions:
        elem = definition.get_text(separator=': ', strip=True)
        elem_clear = elem.split('\t')[-1].strip()
        if elem and elem_clear not in seen_definitions:
            seen_definitions.add(elem_clear)
            definitions_clear.append(elem_clear)
    return(definitions_clear)
