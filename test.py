import json


with open('intents/phrases.json', encoding='utf-8') as file:
    file = json.load(file)

for theme, phrases in file.items():
    print()