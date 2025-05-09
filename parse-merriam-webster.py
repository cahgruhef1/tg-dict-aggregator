import re
import requests
from bs4 import BeautifulSoup


def parse_merriam_webster(word: str):
    TEMPLATE_URL = "https://www.merriam-webster.com/dictionary/"
    request_url = TEMPLATE_URL + word.lower()
    response = requests.get(request_url)
    bs = BeautifulSoup(response.text, "html.parser")
    definition = bs.find_all("span", "dtText")
    definitions = [re.sub(": ", "", elem.text) for elem in definition]
    if len(definitions) != 0:
        return "; ".join(definitions)
    return "Word not found."


if __name__ == "__main__":
    print(parse_merriam_webster(input()))

