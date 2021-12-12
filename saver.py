import argparse
from code import TRANS

parser = argparse.ArgumentParser(description='Zapisuje plik po konwersji')
parser.add_argument('key', help='Klucz ')
parser.add_argument('back', help='Plik tło')
parser.add_argument('data', help='Plik z kodem')

args = parser.parse_args()

new = []
with open(args.back, 'r', encoding='utf8') as background:
    with open(args.data, 'rb') as byts:
        for i in byts.read():
            for j in format(i, '08b'):
                while (token := background.read(1)) not in TRANS:
                    new.append(token)
                if j == '1':
                    new.append(TRANS[token])
                else:
                    new.append(token)

    new.append(background.read())
print("".join(new))
