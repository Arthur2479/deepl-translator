import json
from pprint import pprint

import requests
from bs4 import BeautifulSoup

# URL of the website you want to query
URL = "https://www.wordreference.com/"
FILE_PATH = "words_en.json"
OUTPUT_FILE_PATH = "flashcards.txt"


def main(word_to_test: str, dictionnary: str = 'enfr'):
    response = requests.get(URL + dictionnary + '/' + word_to_test)

    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return

    page_content = response.text

    # Parse the HTML with BeautifulSoup and find the translation table
    soup = BeautifulSoup(page_content, 'html.parser')
    links = soup.find_all('table', class_='WRD')

    # Make sure we are iterating on the wanted table
    assert (links[0].find('tr').find('td').get_text(strip=True) == "Principales traductions")

    lines = links[0].find_all('tr')

    translations = []
    for line in lines[2:]:
        # If new meaning is found, create a new line
        if not line.get('id'):
            # print(f"\nEMPTY ID ! : {line.get('id')}")
            continue

        translation_element = line.find_all('td')[-1]
        # Filter unwanted elements such as examples
        if translation_element.get('class')[0] != 'ToWrd':
            translation_element.decompose()
            continue

        # Filter unwanted elements such as word type
        if translation_element.find_all('em'):
            [element.decompose() for element in translation_element.find_all('em')]

        if translation_element.find_all('a'):
            [element.decompose() for element in translation_element.find_all('a')]

        if translation_element.find_all('span'):  # TODO : keep spans with [qqn] for eg
            [element.decompose() for element in translation_element.find_all('span')]

        translations.append(translation_element.get_text().strip())

    return word_to_test, set(translations)  # Remove duplicates


if __name__ == "__main__":
    with open(FILE_PATH, 'r') as json_file:
        words = json.load(json_file)

    with open(OUTPUT_FILE_PATH, 'a', encoding='utf-8') as output_file:
        for word in words:
            flashcard = main(word)
            print(f'{flashcard[0]}\t{", ".join(flashcard[1])}', file=output_file)
            print(f'{flashcard[0]}\t{", ".join(flashcard[1])}')
