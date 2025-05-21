import requests
import json


def get_word_of_the_day(id, level):
    """
    Get word of the day
    """
    REQUEST_URL = f"https://raw.githubusercontent.com/cahgruhef1/tg-dict-aggregator/refs/heads/main/{level}_word_list.json"
    response = requests.get(REQUEST_URL)
    data = json.loads(response.text)
    keys = data.keys()
    keys = [int(key) for key in keys]
    max_id = max(keys)
    if id <= max_id:
        return data[str(id)]
    return False


if __name__ == "__main__":
    print(get_word_of_the_day(8, "b1"))

