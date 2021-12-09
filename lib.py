import requests
from functools import lru_cache
from bs4 import BeautifulSoup
from pprint import pprint

@lru_cache()
def slownik(litera: str, dlugosc: int) -> list[str]:
    content = requests.get(f'https://polski-slownik.pl/wszystkie-slowa-jezyka-polskiego.php?id={dlugosc}-literowe-na-litere-{litera}')
    slowa = BeautifulSoup(content.text).find_all('p', class_='mbr-text mbr-fonts-style align-center display-7')
    return [i.text.strip('\n') for i in slowa]

def in_slownik(slowo: str) -> bool:
    return slowo in slownik(slowo[0], len(slowo))

if __name__=='__main__':
    pprint(slownik('a', 3))
    