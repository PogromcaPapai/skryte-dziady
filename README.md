# skryte-dziady
Cryptographic and steganographic algorithm that embeds information in polish orthographic mistakes

# Uruchamianie programu

Program wymaga posiadania zainstalowanego Pythona (pisałem go korzystając z wersji 3.10, ale każda młodsza od 3.8.0 także powinna zadziałać). 

[Download Python](https://www.python.org/downloads/)

Zalecane jest także posiadanie biblioteki `tqdm` możliwej do zainstalowania komendą `python -m pip install tqdm`. Zapewnia ona jedynie ładne paski postępu. Aby uruchomić program, wpisujemy będąc w jego folderze w linii komend: `python saver [KLUCZ] [TEKST W KTÓRYM OSADZONE BĘDĄ DANE] [DANE DO OSADZENIA]`. Dostępne jest także więcej opcji:

- `-h` udostępnia pomoc dla użytkownika,
- `-o` umożliwiające podanie pliku, do którego wynik ma być zapisany,
- `--volume`, dzięki któremu program określi najpierw pojemność pliku.

Aby uruchomić skrypt do odszyfrowywania, wpisujemy `python loader [KLUCZ] [PLIK WYNIKOWY] [PLIK WYJŚCIOWY]`. Tutaj dostępna jest tylko opcja `-h`.

<aside>
💡 W folderze <code>zrodla</code> zamieściłem zestaw przykładowych plików do testów.

</aside>

[Więcej informacji](https://www.notion.so/notorycznenotatki/Projekt-zaliczeniowy-dokumentacja-f0701ba9fc3f4905859f875d2ae2a9c6)