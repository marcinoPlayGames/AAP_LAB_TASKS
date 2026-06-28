# Discord RAG Moderator

Inteligentny bot moderacyjny dla Discorda wykorzystujący architekturę **RAG (Retrieval-Augmented Generation)** oraz model językowy Gemini do wspomagania administratorów w podejmowaniu decyzji moderacyjnych.

Projekt został wykonany w ramach przedmiotu **Architektura aplikacji Python**.

---

# Funkcjonalności

* analiza zgłoszeń moderatorów z wykorzystaniem AI,
* wyszukiwanie informacji w lokalnym regulaminie (PDF),
* wyszukiwanie odpowiednich kar w taryfikatorze (XLSX),
* generowanie rekomendacji na podstawie architektury RAG,
* możliwość natychmiastowego wykonania sugerowanej kary z poziomu Discorda,
* historia decyzji AI zapisywana w bazie SQLite,
* system uprawnień (RBAC) ograniczający dostęp do komend administracyjnych,
* możliwość przeładowania dokumentów bez restartowania bota.

---

# Wykorzystane technologie

* Python 3
* discord.py
* Google Gemini API
* pandas
* RapidFuzz
* SQLite
* pypdf

---

# Architektura projektu

```
bot/
│
├── checks/
│   └── permissions.py
│
├── cogs/
│   ├── advisor.py
│   ├── moderation.py
│   └── history.py
│
├── views/
│   └── moderation_buttons.py
│
data/
│   ├── regulamin.pdf
│   ├── taryfikator.xlsx
│   └── decisions.db
│
parsers/
│   ├── pdf_parser.py
│   └── excel_parser.py
│
services/
│   ├── ai_service.py
│   ├── database.py
│   ├── moderation_service.py
│   └── rag.py
│
config.py
main.py
requirements.txt
README.md
```

---

# Jak działa RAG?

1. Administrator opisuje sytuację za pomocą komendy:

```
/ask
```

2. Bot przeszukuje:

* regulamin zapisany w pliku PDF,
* taryfikator zapisany w pliku XLSX.

3. Najbardziej pasujące fragmenty zostają przekazane do modelu Gemini jako kontekst.

4. Model generuje odpowiedź zawierającą:

* analizę sytuacji,
* proponowaną karę,
* uzasadnienie decyzji.

5. Moderator może od razu wykonać sugerowaną akcję przyciskiem:

* Mute
* Kick
* Ban

---

# Dostępne komendy

## Moderacja

```
/mute
```

Wyciszenie użytkownika.

```
/kick
```

Usunięcie użytkownika z serwera.

```
/ban
```

Zbanowanie użytkownika.

---

## AI

```
/ask
```

Analiza zgłoszenia przy użyciu architektury RAG oraz modelu Gemini.

```
/reload_documents
```

Przeładowanie plików regulaminu i taryfikatora bez restartowania bota.

---

## Historia

```
/history
```

Wyświetlenie historii decyzji AI.

---

# Konfiguracja

Utwórz plik `.env`:

```env
DISCORD_TOKEN=YOUR_DISCORD_TOKEN
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
GUILD_SERVER_ID=YOUR_GUILD_ID
```

---

# Instalacja

Sklonuj repozytorium:

```bash
git clone <adres_repozytorium>
cd Discord-Rag-Moderator
```

Zainstaluj zależności:

```bash
pip install -r requirements.txt
```

Uruchom bota:

```bash
python main.py
```

---

# Wymagane pliki

Projekt wymaga obecności katalogu `data` zawierającego:

```
regulamin.pdf
taryfikator.xlsx
```

Na ich podstawie moduł RAG wyszukuje informacje wykorzystywane przez model językowy.

---

# Baza danych

Historia decyzji AI przechowywana jest lokalnie w bazie SQLite:

```
data/decisions.db
```

Zapisywane są:

* moderator,
* treść zgłoszenia,
* odpowiedź AI,
* data wykonania.

---

# Autor

Marcin Pawłowski