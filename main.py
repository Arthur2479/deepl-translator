import requests


def load_api_key(file_path):
    """Load the DeepL API key from a file."""
    try:
        with open(file_path, 'r') as file:
            api_key = file.read().strip()
        return api_key
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None


def translate_text(text, target_language, api_key):
    """Translate text using the DeepL API."""
    url = 'https://api-free.deepl.com/v2/translate'
    headers = {
        'Authorization': f'DeepL-Auth-Key {api_key}',
    }
    data = {
        'text': text,
        'target_lang': target_language,
        'formality': 'default'
    }
    response = requests.post(url, headers=headers, data=data)

    if response.status_code == 200:
        result = response.json()
        return result
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None


def main():
    api_key_file = 'api_key_deepl.txt'  # Path to the file containing the API key
    api_key = load_api_key(api_key_file)

    if api_key is None:
        return

    # Text to translate
    text = "run"

    # Target language, e.g., 'DE' for German, 'FR' for French, etc.
    target_language = 'FR'

    # Translate the text
    translated_text = translate_text(text, target_language, api_key)

    if translated_text:
        print(f"Original text: {text}")
        print(f"Translated text: {translated_text}")


if __name__ == "__main__":
    main()
