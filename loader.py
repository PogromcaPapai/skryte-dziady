import argparse
from lib import *

parser = argparse.ArgumentParser(description='Odszyfrowuje wiadomość w postaci błędów ortograficznych')
parser.add_argument('key', help='Klucz', type=int)
parser.add_argument('input', help='Plik z szyfrem')
parser.add_argument('output', help='Plik docelowy')

args = parser.parse_args()
seed(args.key)

with open(args.input, 'r', encoding='utf8') as data:
    decoded = decode_text(data.read())

with open(args.output, 'wb') as new:
    for i in decoded:
        new.write(i)
