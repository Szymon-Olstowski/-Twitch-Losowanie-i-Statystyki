# Twitch Losowanie i Statystyki
Aplikacja webowa do losowania widzów i wyświetlania statystyk kanałów Twitch.

## Wymagania systemowe
- Python 3.11.5 lub nowszy
- Przeglądarka internetowa
- Konto na platformie Twitch

## Struktura projektu

**Pliki główne:**
* **main.py** - Główny plik aplikacji Flask, odpowiedzialny za uruchomienie serwera i obsługę routingu
* **twitch_bot.py** - Bot Twitch, służący do interakcji z czatem i wykonywania komend
* **requirements.txt** - Lista zależności projektu
* **.env** - Plik konfiguracyjny ze zmiennymi środowiskowymi
* **channels.txt** - Lista kanałów Twitch do monitorowania

**Katalog templates/**:
* **index.html** - Strona główna aplikacji
* **los.html** - Strona losowania elementów
* **clips.html** - Strona wyświetlająca klipy
* **channel_stats.html** - Statystyki kanału
* **nav.html** - Wspólna nawigacja dla wszystkich stron

## Instrukcja instalacji

1. Zainstaluj wymagane pakiety:
```bash
pip install -r requirements.txt
```
2. Skomfigurować plik .env

3. W pliku channels.txt są przechowywane nazwy kanałów do losowania i zmiany trzeba robić przed uruchomieniem strony
# Poradnik: Jak stworzyć token do bota z Twitcha
``` txt
TOKEN=twój_token_twitch
PREFIX=!
TWITCH_CLIENT_ID=twoje_client_id
TWITCH_CLIENT_SECRET=twój_secret
HOST=Tu możesz ustawić własny host. Domyślnie ustawiony na 127.0.0.1
PREFIX= Tu mozesz ustawić własny prefic. Domyśle ustawiony zt.
```
## Krok 1: Generowanie tokena
1. Otwórz przeglądarkę i przejdź do [Twitch Token Generator](https://twitchtokengenerator.com/quick/vR5wTrOJ15).
2. Zaloguj się na swoje konto Twitch.
3. Kliknij przycisk "Generate Token".
4. Skopiuj wygenerowany token i zapisz go w pliku: .env.

## Krok 2: Używanie tokena w swoim bocie
1. W kodzie swojego bota, wklej skopiowany token w pliku: .env.
2. Upewnij się, że token jest używany do odczytywania i wysyłania wiadomości.
3. Dodaj nazwy kanałów do pliku channels.txt (każda nazwa w nowej linii) wymagane do losowania uzytkowników

## Krok 4: Uruchom aplikcję
```bash
python main.py
```
# Poradnik: Jak uzyskać dostęp do Twitch API

## Krok 1: Rejestracja aplikacji
1. Przejdź do [Twitch Developer Portal](https://dev.twitch.tv/console/apps).
2. Zaloguj się na swoje konto Twitch.
3. Kliknij przycisk "Register Your Application".
4. Wypełnij formularz rejestracyjny:
    - **Name**: Nazwa Twojej aplikacji.
    - **OAuth Redirect URLs**: Wpisz adres: https://localhost
    - **Category**: Wybierz kategorię Other
5. Kliknij "Create".

## Krok 2: Uzyskanie Client ID i Client Secret
1. Po zarejestrowaniu aplikacji, przejdź do jej ustawień.
2. Skopiuj **Client ID** i **Client Secret** i wpisz je w pliku .env
