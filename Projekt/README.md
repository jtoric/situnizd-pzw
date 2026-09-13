# Powerlifting Competition Registrations

Sustav za prijavu natjecatelja na powerlifting natjecanja.  
Projekt za kolegij **Razvoj web aplikacija** — SIT UNIZD.

---

## Tehnologije

| Sloj     | Stack                                  |
|----------|----------------------------------------|
| Backend  | Python 3.11+, FastAPI, SQLAlchemy 2.0  |
| Baza     | PostgreSQL 16 (Docker Compose)         |
| Frontend | Vue 3, TypeScript, Pinia, Vue Router   |
| Auth     | JWT (access + refresh tokeni)          |

---

## Preduvjeti

- **Python** ≥ 3.11 — [python.org/downloads](https://www.python.org/downloads/)
- **Node.js** ≥ 18 — [nodejs.org](https://nodejs.org/)
- **Docker Desktop** — [docker.com/products/docker-desktop](https://www.docker.com/products/docker-desktop/)
- **Git** — [git-scm.com](https://git-scm.com/)

---

## Pokretanje

### 1. Kloniraj repo i kopiraj env varijable

```bash
git clone <url>
cd <repo>

# Linux/macOS:
cp .env.example .env

# Windows (PowerShell):
Copy-Item .env.example .env
```

### 2. Pokreni PostgreSQL bazu

```bash
docker compose up -d db
```

### 3. Pokreni backend

```bash
cd api

# Kreiraj virtualno okruženje (jednom):
python -m venv .venv

# Aktiviraj:
# Linux/macOS:         source .venv/bin/activate
# Windows PowerShell:  .venv\Scripts\Activate.ps1
# Windows cmd:         .venv\Scripts\activate.bat

pip install -r requirements.txt
alembic upgrade head
python -m app.seed

uvicorn app.main:app --reload
```

- API: http://127.0.0.1:8000/health
- Swagger UI: http://127.0.0.1:8000/docs

### 4. Pokreni frontend

```bash
cd web
npm install
npm run dev
```

- App: http://localhost:5173

### Dev kredencijali

| Korisničko ime | Lozinka  | Uloga |
|----------------|----------|-------|
| `admin`        | `admin123` | Admin |
| `behemot`      | `klub123`  | Klub  |
| `heraklo`      | `klub123`  | Klub  |

---

## Struktura projekta

```
repo/
├── api/                          # FastAPI backend
│   ├── app/
│   │   ├── main.py               # App factory
│   │   ├── seed.py               # Seed podaci
│   │   ├── core/                 # Infrastruktura (config, errors, logging)
│   │   ├── routers/              # HTTP sloj
│   │   ├── services/             # Poslovna logika
│   │   ├── repositories/         # DB upiti
│   │   ├── models/               # SQLAlchemy ORM modeli
│   │   └── schemas/              # Pydantic DTO-ovi
│   ├── alembic/                  # Migracije
│   ├── tests/                    # pytest testovi (SQLite in-memory)
│   ├── requirements.txt
│   └── pyproject.toml
├── web/                          # Vue 3 frontend
│   ├── src/
│   │   ├── main.ts               # Bootstrap: Pinia + Router + mount
│   │   ├── App.vue               # Layout switcher (route.meta.layout)
│   │   ├── router/               # Rute s meta: { layout, javno, uloga }
│   │   ├── stores/               # Pinia: auth.ts, obavijesti.ts
│   │   ├── services/             # API pozivi po domeni
│   │   ├── types/                # TypeScript interfejsi
│   │   ├── utils/                # faza.ts, validacija.ts
│   │   ├── layouts/              # LayoutGost.vue, LayoutAplikacija.vue
│   │   ├── components/           # Tablica, FormaPolje, Gumb, Modal...
│   │   └── views/                # admin/ i klub/ viewovi
│   ├── tests/e2e/                # Playwright E2E testovi
│   └── playwright.config.ts
├── .github/workflows/ci.yml      # GitHub Actions CI
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Backend arhitektura

Svaki sloj ima jednu odgovornost. Pravilo: **gornji sloj može zvati donji, ali nikad obrnuto**.

```
  HTTP request
       ↓
  ┌─────────┐
  │ Router   │  Parsira request, poziva service, vraća HTTP response.
  └────┬─────┘  NE sadrži poslovnu logiku.
       ↓
  ┌─────────┐
  │ Service  │  Provodi poslovna pravila (rokovi, vlasništvo, validacija).
  └────┬─────┘  NE zna za HTTP status kodove.
       ↓
  ┌──────────────┐
  │ Repository   │  Izvršava SQL upite, vraća domenske objekte.
  └──────┬───────┘  NE zna za poslovnu logiku.
         ↓
  ┌─────────┐
  │   DB    │  PostgreSQL
  └─────────┘
```

---

## Frontend arhitektura

### Konvencije

- Composition API, `<script setup lang="ts">` svugdje
- Identifikatori i komentari: **hrvatski** — osim public API storeova (`isAuthenticated`, `isAdmin`, `user`, `logout`)
- Strict TypeScript: `noUncheckedIndexedAccess`, `exactOptionalPropertyTypes`
- Nema UI biblioteka — custom CSS s design tokenima

### Routing

- `route.meta.layout`: `'gost'` | `'aplikacija'` — `App.vue` bira layout komponentu
- `route.meta.javno`: `true` za rute bez autentikacije
- `route.meta.uloga`: `'admin'` | `'klub'` za route guards

### State management

- **Store** za dijeljeni state: `auth.ts` (token, korisnik), `obavijesti.ts` (toastovi)
- **Lokalni `ref`** za state koji koristi samo jedan view (lista natjecatelja, forma)

### Design — Iron Press

Brutalistički dizajn inspiriran powerlifting plakatima 70-ih.

| Token | Vrijednost |
|---|---|
| `--boja-pozadina` | `#0e0e0e` |
| `--boja-povrsina` | `#1a1a1a` |
| `--boja-rub` | `#2e2e2e` |
| `--boja-tekst` | `#ede6d3` |
| `--boja-akcent` | `#c8451a` |
| `--boja-uspjeh` | `#7a8c3a` |

Display font: **Big Shoulders Display** — Body font: **JetBrains Mono**

---

## Migracije i baza

```bash
cd api

alembic upgrade head             # Primijeni sve migracije
alembic downgrade -1             # Rollback zadnje migracije
alembic revision --autogenerate -m "opis"  # Nova migracija
python -m app.seed               # Seed podatke u bazu
```

### Reset baze

```bash
docker compose down -v
docker compose up -d db
cd api && alembic upgrade head && python -m app.seed
```

---

## Testovi

### Backend (pytest — SQLite in-memory, bez Dockera)

```bash
cd api
pytest
```

### Frontend (Vitest — unit testovi)

```bash
cd web
npm run test:run
```

### E2E (Playwright — zahtijeva pokrenute oba servera)

```bash
cd web
npm run test:e2e        # headless
npm run test:e2e:ui     # Playwright UI
```

---

## Git konvencije

Format poruke: `<tip>(<scope>): <opis>`

| Tip        | Značenje                          |
|------------|-----------------------------------|
| `feat`     | Nova funkcionalnost               |
| `fix`      | Ispravka buga                     |
| `refactor` | Promjena bez nove funkcionalnosti |
| `test`     | Testovi                           |
| `chore`    | Tooling, config, infrastruktura   |
| `docs`     | Dokumentacija                     |

Scope: `api`, `web`, `ci` — ili prazan za root-level promjene.

---

## Env varijable

- `.env.example` — ključevi s demo vrijednostima, **ide u git**
- `.env` — stvarne vrijednosti, **NE ide u git**
- U produkciji: env varijable dolaze iz platforme (Railway/Render)
