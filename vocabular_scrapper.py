import json
import random
from pprint import pprint

import requests
from bs4 import BeautifulSoup

# URL of the website you want to query
URL = "http://www.wordcyclopedia.com/english/c1"
FILE_PATH = "words_en.json"


def main():
    response = requests.get(URL)

    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return

    page_content = response.text

    # Parse the HTML with BeautifulSoup and find the translation table
    soup = BeautifulSoup(page_content, 'html.parser')
    words = soup.find_all('div', class_='cefrWord')

    return [word.get_text(strip=True) for word in words]


if __name__ == "__main__":
    words_found = main()
    print(f'Word count : {len(words_found)}')
    random.shuffle(words_found)
    pprint(words_found)

    with open(FILE_PATH, 'w') as json_file:
        json.dump(words_found, json_file)
