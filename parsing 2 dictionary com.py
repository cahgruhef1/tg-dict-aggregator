import requests
from bs4 import BeautifulSoup


def parse_dictionary_com(word: str):
    TEMPLATE_URL = 'https://www.dictionary.com/browse/'
    request_url = TEMPLATE_URL + word.lower()
    response = requests.get(request_url)
    bs = BeautifulSoup(response.text, "html.parser")
    definitions = bs.find_all('div', 'NZKOFkdkcvYgD3lqOIJw')
    if len(definitions) != 0:
        definition = bs.find_all('div', 'NZKOFkdkcvYgD3lqOIJw')[0].text.split('<!-- -->')[0]
        return definition
    return False
