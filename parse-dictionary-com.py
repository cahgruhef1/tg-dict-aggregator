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
    return "Word not found."


if __name__ == "__main__":
    print(parse_dictionary_com(input()))

