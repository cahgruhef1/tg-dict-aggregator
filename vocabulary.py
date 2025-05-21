from bs4 import BeautifulSoup
import requests


def get_vocabulary_definition(word):
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
    definitions_clear = []
    seen_definitions = set()
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

            result.append({
                "definitions": elem_clear,
                "synonyms": synonyms_clear,
                "examples": examples_clear,
            })

    return(result)
