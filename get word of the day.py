import requests
from bs4 import BeautifulSoup
import random
import json


request_c1 = requests.get('https://www.esl-lounge.com/student/reference/a1-cefr-vocabulary-word-list.php')
bs = BeautifulSoup(request_c1.text, 'html.parser')
word_lists = list(bs.find_all('td', 'left'))
#print(type(a_list[0]))
#a_list = [str(word).strip() for word in a_list if str(word) != '<br/>']
#print(a_list)

lexemes = []

for word_list in word_lists:
    lexemes.extend([str(word).strip() for word in word_list if str(word) != '<br/>'])

random.shuffle(lexemes)
ids = [i + 1 for i in range(len(lexemes))]
lexemes_with_ids = dict(zip(ids, lexemes))
print(lexemes_with_ids)

with open('a1_word_list.json', 'w') as output:
    json.dump(lexemes_with_ids, output)
