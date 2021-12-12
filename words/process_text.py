from json import dump

words = []

with open('words/odm.txt', 'r', encoding='utf-8') as f:
    for i in f.readlines():
        words += [j for j in i.removesuffix('\n').split(', ') if " " not in j]

with open('words/processed.json', 'w') as f:
    dump(words, f)