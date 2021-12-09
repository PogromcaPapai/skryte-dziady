import argparse
from code import TRANS

parser = argparse.ArgumentParser(description='Zapisuje plik po konwersji')
parser.add_argument('back', help='Plik tło', default='zrodla\\dziady3.txt')
parser.add_argument('data', help='Plik z kodem', default='zrodla\\to_code.txt')

args = parser.parse_args()

with open('new.txt', 'w', encoding='utf8') as new:
    with open(args.back, 'r', encoding='utf8') as background:
        with open(args.data, 'rb') as byts:
            for i in byts.read():
                for j in format(i, '08b'):
                    while (token := background.read(1)) not in TRANS:
                        new.write(token)
                    if j == '1':
                        new.write(TRANS[token])
                    else:
                        new.write(token)

        new.write(background.read())
