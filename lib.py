from json import load as _jsonload
from re import compile as _regcomp, escape as _rescape
from random import Random
from typing import Iterable, Match
from cipher import TRANS

PUNCTUATIONS = '''!()-[]{};:'"\,<>./?@#$%^&*_~'''
PATTERN = _regcomp("(?P<coding>"+"|".join(["(%s)" % i for i in TRANS.keys()])+')|.')

with open('words/processed.json', 'r') as f:
    WORDS = set(_jsonload(f))

rnd = Random()

def seed(x):
    rnd.seed(x)

# HELPERS

def whole(m: Match) -> str:
    return m.group(0)
    
def _rem_punctuation(word: str)-> str:
    for i in PUNCTUATIONS:
        word = word.replace(i, f" {i} ")
    return word

def _add_punctuation(word: str)-> str:
    for i in PUNCTUATIONS:
        word = word.replace(f" {i}", i)
        if i not in ',.:!?%;':
            word = word.replace(f"{i} ", i)
    return word


# GENERAL

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
randoms = 0
def find_zero(word):
    global randoms
    try:
        return ZEROS[word], False
    except KeyError:
        absclass = equivalent(word)
        exist = [i for i in absclass if i in WORDS]
        if exist:
            exist.sort()
            zero = rnd.choice(exist)
            # print(exist, absclass, zero)
            randoms += 1
            not_code = False
        else:
            zero = word
            not_code = True
        for i in absclass:
            ZEROS[i] = zero
        return zero, not_code


# LOADING

def decode(zero, word) -> list[bool]:
    l = []
    for z, w in zip(PATTERN.finditer(zero), PATTERN.finditer(word)):
        if w.group('coding'):
            l.append(whole(z) != whole(w))
    return l

def _convert(toconv: list[bool]) -> list[bytes]:
    byte = 0; length = 0
    for i in toconv:
        byte *= 2
        byte += i
        if (length := length+1) == 8:
            yield bytes([byte])
            byte = 0; length = 0
     
def convert(toconv: list[bool]) -> list[bool]:
    count_zero = 0
    l = []
    for b in _convert(toconv):
        l.append(b)    
        if b != b'\x00':
            count_zero = 0
        else:
            count_zero += 1
    for _ in range(count_zero):
        l.pop(-1)
    return l
        
       
def decode_text(text: str) -> list[bytes]:
    data = []
    for i in text.split('\n'):
        for j in _rem_punctuation(i).split():
            zero, not_coding = find_zero(j)
            if not not_coding:
                converted = decode(zero, j)
                data.extend(converted)
    return convert(data)
                                    

# SAVING

def encode_text(text: str, bytes_: str):
    list_bytes = [i == "1" for i in bytes_]
    words = []
    for i in text.split('\n'):
        line = []
        if not list_bytes:
            # words.append(i)
            # continue
            break
        for j in _rem_punctuation(i).split():
            if not list_bytes:
                line.append(j) 
                continue
            zero, not_coding = find_zero(j)
            if not_coding:
                line.append(zero)
            else:
                added, list_bytes = encode(zero, list_bytes)
                if j.istitle():
                    line.append(added.capitalize())
                else:
                    line.append(added)                
        words.append(_add_punctuation(" ".join(line)))
    return "\n".join(words)  
        
def encode(word: str, byt: list[bool]):
    w = []
    for i in PATTERN.finditer(word):
        if i.group('coding') and byt and byt.pop(0):
            w.append(TRANS[whole(i)])
        else:
            w.append(whole(i))
    return "".join(w), byt
    
if __name__ == "__main__":
    from time import perf_counter_ns
    # seed(123)
    # seed(3232)
    words = 'studniówka', 'test', 'Bóg', "źdźbło", "brzęczy", "chrząszcz", "gęślą"
    
    for word in words:
        start = perf_counter_ns()
        zero, _ = find_zero(word)
        end = perf_counter_ns()
        eq = equivalent(word)
        print(zero, (end-start)/1000, [i for i in eq if i in WORDS], eq, sep='\t')