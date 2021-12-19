from json import load as _jsonload
from re import T, compile as _regcomp
from random import Random
from typing import Match
from collections import Counter

from cipher import TRANS
from tqdm import tqdm

PUNCTUATIONS = """$¢‘⁄\\‡°{⁂&′,·>§*’¦._№¶—¥₪"}?@–¬(%…[„―‐¡‽␠<|‱∴¤☞‰€/¨-:!«¿;#•£“※\'‒^₩)~»]”†"""
PATTERN = _regcomp("(?P<coding>"+"|".join(["(%s)" % i for i in TRANS.keys()])+')|.')

debug = None
def logger(name):
    global debug
    debug = open('%s.log' % name, 'w', encoding='utf8')


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

# GENERAL

def count_volume(words: str) -> int:
    matches = PATTERN.findall(words)
    counted = Counter(i[0] for i in matches)
    del counted['']
    return sum(counted.values())//8

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
        val = ZEROS[word]
        print("found:", val, file=debug)
        return val, False
    except KeyError:
        absclass = equivalent(word)
        exist = [i for i in absclass if i in WORDS]
        if exist:
            exist.sort()
            zero = rnd.choice(exist)
            print('genze:', exist, sorted(absclass), zero, file=debug)
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
            print('write:', whole(z), whole(w), l[-1], file=debug)
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
    data: list[bool] = []
    for i in tqdm(text.split('\n')):
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
    old_len = len(list_bytes)
    progress = tqdm(total=old_len)
    try:
        for i in text.split('\n'):
            progress.update(old_len-len(list_bytes))
            old_len = len(list_bytes)
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
            words.append(" ".join(line))
    except KeyboardInterrupt:
        pass
    return "\n".join(words)  
        
def encode(word: str, byt: list[bool]):
    w = []
    for i in PATTERN.finditer(word):
        if i.group('coding') and byt:
            if byt.pop(0):
                w.append(TRANS[whole(i)])
                print('write:', whole(i), TRANS[whole(i)], True, file=debug)
            else:
                w.append(whole(i))
                print('write:', whole(i), whole(i), False, file=debug)
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