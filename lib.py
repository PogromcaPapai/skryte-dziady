from json import load as _jsonload
from re import compile as _regcomp
from random import choice as _choice, seed
from typing import Match
from cipher import TRANS

PATTERN = _regcomp("(?P<coding>"+"|".join(["(%s)" % i for i in TRANS.keys()])+')|.')

with open('words/processed.json', 'r') as f:
    WORDS = _jsonload(f)

def process_words(text: str, bytes_: str):
    list_bytes = [i == "1" for i in bytes_]
    words = []
    for i in text.split('\n'):
        line = []
        for j in i.split():
            zero = find_zero(j)
            added, list_bytes = encode(zero, list_bytes)
            line.append(added)
        words.append(" ".join(line))
    return "\n".join(words)
                
        
def encode(word: str, byt: list[bool]):
    w = []
    for i in PATTERN.finditer(word):
        if i.group('coding') and byt and byt.pop(0):
            w.append(TRANS[str(i)])
        else:
            w.append(str(i))
    return "".join(w), byt

def whole(m: Match) -> str:
    return m.group(0)

def _equivalent(found: list[str]):
    w = []
    while found:
        i = found.pop(0)
        if i.group('coding'):
            return sum(([w+[whole(i)]+j, w+[TRANS[whole(i)]]+j] for j in _equivalent(found[:])), [])
        else:
            w.append(whole(i))
    return [w]

def equivalent(word: str) -> list[str]:
    found = list(PATTERN.finditer(word))
    return ["".join(i) for i in _equivalent(found[:])]

ZEROS = {}
def find_zero(word):
    try:
        return ZEROS[word]
    except KeyError:
        absclass = equivalent(word)
        exist = [i for i in absclass if i in WORDS]
        zero = word if not exist else _choice(exist)
        for i in absclass:
            ZEROS[i] = zero
        return zero
    
if __name__ == "__main__":
    # seed(123)
    # seed(3232)
    words = 'studniówka', 'test', 'Bóg'
    
    for word in words:
        print(equivalent(word))
        print(find_zero(word))