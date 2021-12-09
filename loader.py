import argparse
from code import TRANS
from io import TextIOWrapper

parser = argparse.ArgumentParser(description='Zapisuje plik po konwersji')
parser.add_argument('org', help='Plik tło')
parser.add_argument('data', help='Plik z kodem')

args = parser.parse_args()

def zp(a: TextIOWrapper, b: TextIOWrapper):
    while a.readable() and b.readable():
        yield a.read(1), b.read(1)

with open('translated.txt', 'wb') as new:
    counter = 0
    with open(args.org, 'r', encoding='utf8') as original:
        with open(args.data, 'r', encoding='utf8') as data:
            byte = 0; l = 0
            for i, j in zp(original, data):
                if i in TRANS:
                    byte *= 2
                    byte += (i != j)
                    if (l := l+1) == 8:
                        c = bytes([byte])
                        if c != b'\x00':
                            new.write(c)
                        else:
                            counter += 1
                        byte = 0; l = 0
                if counter > 10:
                    break
                