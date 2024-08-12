# About

Flipper catalog downloader

# Development

## Requirements

For development:

- Python 3.11
- Poetry

### MacOS
- Python 3.11
  - `brew install python@3.11`
- Poetry
  - `pip install poetry`
  
## Running application

Download source code for applications specific sdk

`python main.py download_builds --output some --api 69.0 --target f7`

Generate words

`poetry run python main.py gen -m models/*.pt -w inputs/*.txt -o outputs/words.txt -a 1000`

Leet-converter

`poetry run python main.py leet -w outputs/words.txt -o outputs/leet_words.txt`

Filter words

`poetry run python main.py filter -s inputs/offensive_words.pkl -w outputs/leet_words.txt -o outputs/filtered_words.txt`
