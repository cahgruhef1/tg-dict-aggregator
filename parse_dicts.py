import re
import requests
from bs4 import BeautifulSoup


def parse_dictionary_com(word: str):
    """
    Parse dictionary.com
    """
    TEMPLATE_URL = "https://www.dictionary.com/browse/"
    request_url = TEMPLATE_URL + word.lower()
    response = requests.get(request_url)
    bs = BeautifulSoup(response.text, "html.parser")
    definitions = bs.find_all("div", "NZKOFkdkcvYgD3lqOIJw")
    if len(definitions) != 0:
        definition = definitions[0].text.split("<!-- -->")[0]
        return definition + "\n Source: dictionary.com"
    raise KeyError("Word not found.")


def parse_merriam_webster(word: str):
    """
    Parse Merriam Webster
    """
    TEMPLATE_URL = "https://www.merriam-webster.com/dictionary/"
    request_url = TEMPLATE_URL + word.lower()
    response = requests.get(request_url)
    bs = BeautifulSoup(response.text, "html.parser")
    definition = bs.find_all("span", "dtText")
    definitions = [re.sub(": ", "", elem.text) for elem in definition]
    if len(definitions) != 0:
        return "; ".join(definitions) + "\n Source: merriam-webster.com"
    raise KeyError("Word not found.")


def parse_oxford(word: str):
    """
    Parse oxfordlearnersdictionaries.com
    """
    TEMPLATE_URL = "https://www.oxfordlearnersdictionaries.com/us/definition/american_english/"
    HEADERS = {"User-Agent": "Mozilla/5.0"}
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
            if "<" not in str(elem):
                definition_clear.append(str(elem))
            else:
                if "<" not in str(elem):
                    definition_clear.append(str(elem.contents[0]))
                else:
                    definition_clear.append(" " + elem.contents[0].text)
        definitions_clear.append(re.sub(r"\s{2,}", " ", "".join(definition_clear)))
    return "; ".join(definitions_clear) + "\n Source: oxfordlearnersdictionaries.com"


def parse_vocabulary(word):
    """
    Get a definition from vocabulary.com
    """
    result = []
    url = f"https://www.vocabulary.com/dictionary/{word}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        raise KeyError("Word not available.")
    bs = BeautifulSoup(response.text, "html.parser")
    definitions = bs.find_all("div", class_="definition")
    definitions = [definition for definition in definitions if definition.find_all("div", class_="pos-icon")]
    if len(definitions) == 0:
        raise KeyError("Word not found.")
    seen_definitions = set()
    res_defs = []
    res_syn = []
    res_ex = []
    for definition in definitions:
        elem = definition.get_text(separator=": ", strip=True)
        elem_clear = elem.split("\t")[-1].strip()
        if elem and elem_clear not in seen_definitions:
            seen_definitions.add(elem_clear)

            parent_block_definition = definition.parent
            if parent_block_definition:
                synonyms_clear = []
                synonyms_1 = parent_block_definition.find("span", class_="detail", string="synonyms:")
                if synonyms_1:
                    synonyms_2 = synonyms_1.find_next("span")
                    if synonyms_2:
                        synonyms = synonyms_2.find_all("a", class_="word")
                        synonyms_clear = [elem_synonyms.get_text(strip=True) for elem_synonyms in synonyms]

                examples_clear = []
                examples = parent_block_definition.find_all("div", class_="example")
                for example in examples:
                    example_clear = example.get_text(" ", strip=True)
                    example_clear = example_clear.strip('"')
                    examples_clear.append(example_clear)

            if elem_clear is not None:
                res_defs.append(elem_clear)
            if synonyms_clear is not None:
                res_syn.append(", ".join(synonyms_clear))
            if examples_clear is not None:
                res_ex.append(". ".join(examples_clear))

    return "Definitions: " + "; ".join(res_defs) + "\n" + \
           "Synonyms: " + "; ".join(res_syn) + "\n" + \
           "Examples: " + "; ".join(res_ex) + "\n" + \
           "Source: vocabulary.com"


def parse_wiktionary(word: str):
    """
    Parse en.wiktionary.org
    """
    REQUEST_TEMPLATE = "https://api.dictionaryapi.dev/api/v2/entries/en/"
    result = eval(requests.get(REQUEST_TEMPLATE + word).text)
    try:
        definition = result[0]["meanings"][0]["definitions"][0]["definition"]
    except KeyError:
        raise KeyError("Word not found.")
    return definition + "\n Source: wiktionary.com"


if __name__ == "__main__":
    word = input()
    print(parse_dictionary_com(word))
    print(parse_merriam_webster(word))
    print(parse_oxford(word))
    print(parse_vocabulary(word))
    print(parse_wiktionary(word))

