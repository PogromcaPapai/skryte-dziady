import argparse
from lib import *

parser = argparse.ArgumentParser(description='Szyfruje wiadomość w postaci błędów ortograficznych')
parser.add_argument('key', help='Klucz', type=int)
parser.add_argument('input', help='Plik startowy')
parser.add_argument('data', help='Plik z kodem')
parser.add_argument('--output', help='Plik docelowy')

args = parser.parse_args()
seed(args.key)

with open(args.input, 'r', encoding='utf8') as background:
    with open(args.data, 'rb') as byts:
        data = sum(([j for j in format(i, '08b')] for i in byts.read()), [])
        encoded = encode_text(background.read(), data)

if args.output:
    with open(args.output, 'w', encoding='utf8') as new:
        new.write(encoded)
else:
    print(encoded)
