import requests
from bs4 import BeautifulSoup

def get_word_details(word):
    """
    Get definitions, synonyms, and examples from Collins Dictionary
    """

    urls = {
        "definition": f"https://www.collinsdictionary.com/dictionary/english/{word}",
        "thesaurus": f"https://www.collinsdictionary.com/dictionary/english-thesaurus/{word}",
        "examples": f"https://www.collinsdictionary.com/sentences/english/{word}"
    }

    details = {
        "word": word,
        "definitions": [],
        "synonyms": [],
        "examples": []
    }

    # Get definitions
    try:
        headers={'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
        response = requests.get(urls["definition"], headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        print(response.text)

        for definition in soup.find_all("div", class_="sense"):
            meaning = definition.find("span", class_="def")
            if meaning:
                details["definitions"].append(meaning.text.strip())
    except requests.RequestException as e:
        print(f"Error while trying to get {word}: {e}")

    # Get synonyms
    try:
        headers={'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
        response = requests.get(urls["thesaurus"], headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        synonym_section = soup.find("div", class_="synonyms")
        if synonym_section:
            for synonym in synonym_section.find_all("a"):
                details["synonyms"].append(synonym.text.strip())
    except requests.RequestException as e:
        print(f"Error while trying to get {word}: {e}")

    # Get examples
    try:
        headers={'User-Agent': 'Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)'}
        response = requests.get(urls["examples"], headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        for example in soup.find_all("div", class_="example"):
            example_text = example.text.strip()
            details["examples"].append(example_text)
    except requests.RequestException as e:
        print(f"Error while trying to get {word}: {e}")

    return details

# User word lookup
word_to_lookup = input("Enter the word: ")
word_details = get_word_details(word_to_lookup)

# Print out data
if word_details:
    print(f"\nWord: {word_details["word"]}")

    print("\nDefinitions:")
    for definition in word_details["definitions"]:
        print(f" - {definition}")

    print("\nSynonyms:")
    for synonym in word_details["synonyms"]:
        print(f" - {synonym}")

    print("\nExamples:")
    for example in word_details["examples"]:
        print(f" - {example}")
