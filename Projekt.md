## **Predavanje 1 — Backend: arhitektura \+ skeleton \+ dev okruženje** (tag `predavanje-01`)

1. `chore: init monorepo (api, web) with gitignore and readme`

2. `chore: add docker-compose postgres and env example`

3. `chore(api): add requirements and ruff config`

4. `feat(api): bootstrap FastAPI app factory with settings and health check`

5. `feat(api): add logging setup`

6. `feat(api): add AppError and consistent error response format`

7. `docs: add local dev guide and project conventions`

---

## **Predavanje 2 — Backend: DB modeliranje \+ ORM \+ migracije** (tag `predavanje-02`)

1. `feat(api): add async SQLAlchemy engine, session and get_db dependency`

2. `feat(api): add Club and User models with relationship`

3. `chore(api): add Alembic configured for async engine`

4. `feat(api): add initial migration for clubs and users`

5. `feat(api): add idempotent seed command (admin + demo club)`

6. `docs: document database workflow (migrations, seed, reset)`

---

## **Predavanje 3 — Backend: autentikacija (JWT) \+ security osnove** (tag `predavanje-03`)

1. `refactor(api): rename User.email to username, add is_active + migration`

2. `feat(api): add bcrypt password verification`

3. `feat(api): add JWT utilities (create/decode access + refresh tokens)`

4. `feat(api): add auth service with login and refresh endpoints`

5. `feat(api): add get_current_user dependency and /auth/me endpoint`

6. `test(api): add pytest setup with separate test database`

7. `test(api): add auth tests (login, refresh, expired token, protected endpoint)`

---

## **Predavanje 4 — Backend: autorizacija \+ ownership** (tag `predavanje-04`)

1. `feat(api): add require_role dependency factory`

2. `feat(api): add club schemas and repository`

3. `feat(api): add admin club endpoints (create with login account, update, reset-password)`

4. `feat(api): enforce club ownership in service layer (get club, narrowed list)`

5. `chore(api): add second demo club to seed`

6. `test(api): add role and ownership tests (admin/club/cross-club)`

---

## **Predavanje 5 — Backend: API dizajn \+ CRUD svih entiteta \+ validacija** (tag `predavanje-05`)

1. `feat(api): add Lifter, Competition, Registration models + migration`

2. `feat(api): add lifter schemas (create/update/response) with validators`

3. `fix(api): reject explicit null in PATCH bodies instead of failing in the database`

4. `feat(api): implement lifter CRUD (nested /clubs/{club_id}/lifters) with pagination`

5. `feat(api): implement competition CRUD (admin-write, all-read) with deadline validation`

6. `feat(api): implement registration CRUD (nested /competitions/{comp_id}/registrations)`

7. `feat(api): paginate clubs list like other list endpoints`

8. `chore(api): seed demo lifters and competition`

9. `test(api): add CRUD, validation, pagination and ownership tests`

---

## **Predavanje 6 — Backend: poslovna pravila \+ workflow (pred obranu)** (tag `predavanje-06`)

1. `feat(api): add Phase enum and get_competition_phase helper`

2. `test(api): pin registration tests to OPEN phase with freezegun`

3. `feat(api): enforce phase rules on registration create and category update`

4. `feat(api): translate duplicate registration into 409`

5. `feat(api): add withdraw and reactivate endpoints with status transitions and phase check`

6. `test(api): add phase-based tests with freezegun (OPEN/PRELIM_PASSED/CLOSED)`

7. `test(api): add withdrawal, reactivation and duplicate tests`

8. `docs: add API overview, phase matrix, error codes and lecture tags`

---

# **Obrana 1 — (bez commitova, ili eventualno)**

* `chore: tag release for defense-1 (lecture-06-end)`

---

## **Predavanje 7 — Frontend: arhitektura jednostranične aplikacije, router i raspored** (tag `predavanje-07`)

1. `feat(web): scaffold Vue app with TypeScript, Vite, router and Pinia`

2. `feat(web): add types mirroring API response schemas`

3. `docs: document frontend structure, commands and conventions`

---

## **Predavanje 8 — Frontend: komunikacija s API-jem, prijava (JWT) i zaštita ruta** (tag `predavanje-08`)

1. `feat(web): add API client with ApiError, token refresh and dev proxy`

2. `feat(web): add auth store, login view and session restore`

3. `feat(web): guard routes by login and role`

4. `feat(web): add notifications and global error handling`

5. `docs: describe the path of a request through the frontend`

---

## **Predavanje 9 — Frontend: upravljanje stanjem i stanja sučelja (natjecatelji i prijave)** (tag `predavanje-09`)

1. `feat(web): add lifters store and lists with loading, error and empty states`

2. `feat(web): add lifter form with client checks and server field errors`

3. `feat(web): add competition page with registration form, withdraw and reactivate`

4. `docs: describe where frontend state lives and view states`

---

## **Predavanje 10 — Frontend: tablice, filtri, stranice i sučelje organizatora** (tag `predavanje-10`)

1. `feat(web): add admin competition list and form with deadlines in Zagreb time`

2. `feat(web): add admin clubs list and club creation`

3. `feat(web): add registrations table with filter, pages, search, sort, CSV and phase-aware actions`

4. `feat(web): confirm lifter deletion in an accessible dialog`

5. `docs: describe the organizer interface`

---

## **Predavanje 11 — Testiranje cjelovite aplikacije** (tag `predavanje-11`)

1. `test(api): add coverage config that follows async code in greenlets`

2. `test(api): cover registration lookup, deadline update and refresh after deactivation`

3. `test(web): add Vitest and Playwright, unit tests for lib functions`

4. `test(web): test lifters store and token refresh with mocked modules`

5. `test(e2e): add browser tests for login, registration and deadlines with axe`

6. `fix(web): keep scrollable tables keyboard accessible and inside the page`

7. `docs: describe test levels, coverage and browser tests`

---

## **Predavanje 12 — Produkcija: Docker, nginx, CI i postavljanje** (tag `predavanje-12`)

1. `feat(api): production settings, database health check and first organizer account`

2. `build: add Dockerfiles, nginx config and production compose`

3. `test(e2e): check nginx headers, caching and route fallback against the built app`

4. `ci: run backend, frontend and browser tests on every push`

5. `chore: add database backup with restore check`

6. `docs: add production guide and checklist`

7. `chore: keep LF line endings for shell scripts`

---

## **API površina (24 endpointa)**

Svi popisi imaju `limit` (zadano 20, najviše 100) i `offset`.

### Auth (3)
| Metoda | URL | Opis | Pristup |
|--------|-----|------|---------|
| POST | /auth/login | Login (username + password) | javno |
| POST | /auth/refresh | Obnovi access token | refresh token |
| GET | /auth/me | Trenutni korisnik | authenticated |

### Clubs (5)
| Metoda | URL | Opis | Pristup |
|--------|-----|------|---------|
| GET | /clubs | Lista klubova | admin: svi, club: samo svoj |
| POST | /clubs | Kreiraj klub i njegov login račun | admin |
| GET | /clubs/{club_id} | Detalji kluba | ownership |
| PATCH | /clubs/{club_id} | Ažuriraj klub | admin |
| POST | /clubs/{club_id}/reset-password | Resetiraj lozinku kluba | admin |

### Lifters (5)
| Metoda | URL | Opis | Pristup |
|--------|-----|------|---------|
| GET | /clubs/{club_id}/lifters | Lista natjecatelja, filtar gender | ownership + paginacija |
| POST | /clubs/{club_id}/lifters | Dodaj natjecatelja | ownership |
| GET | /clubs/{club_id}/lifters/{id} | Detalji natjecatelja | ownership |
| PATCH | /clubs/{club_id}/lifters/{id} | Ažuriraj natjecatelja | ownership |
| DELETE | /clubs/{club_id}/lifters/{id} | Obriši natjecatelja (409 ako ima prijava) | ownership |

### Competitions (4)
| Metoda | URL | Opis | Pristup |
|--------|-----|------|---------|
| GET | /competitions | Lista natjecanja (s izračunatom fazom) | authenticated |
| POST | /competitions | Kreiraj natjecanje | admin |
| GET | /competitions/{id} | Detalji natjecanja | authenticated |
| PATCH | /competitions/{id} | Ažuriraj natjecanje | admin |

### Registrations (6)
| Metoda | URL | Opis | Pristup |
|--------|-----|------|---------|
| GET | /competitions/{id}/registrations | Lista prijava, filtar status | admin: sve, club: svoje |
| POST | /competitions/{id}/registrations | Nova prijava | ownership, OPEN faza |
| GET | /competitions/{id}/registrations/{id} | Detalji prijave | ownership |
| PATCH | /competitions/{id}/registrations/{id} | Promjena kategorije/totala | ownership, OPEN/PRELIM |
| POST | /competitions/{id}/registrations/{id}/withdraw | Odjava natjecatelja | ownership, OPEN/PRELIM |
| POST | /competitions/{id}/registrations/{id}/reactivate | Vraćanje odjavljene prijave | ownership, OPEN/PRELIM |

### Health (1)
| Metoda | URL | Opis | Pristup |
|--------|-----|------|---------|
| GET | /health | Health check | javno |

### Matrica operacija po fazama

| Operacija | OPEN | PRELIM_PASSED | CLOSED |
|-----------|------|---------------|--------|
| Nova prijava | ✓ | ✗ | ✗ |
| Promjena kategorije | ✓ | ✓ | ✗ |
| Odjava (→withdrawn) i povratak (→active) | ✓ | ✓ | ✗ |
| Pregled prijava | ✓ | ✓ | ✓ |

### IPF težinske kategorije

- **Muškarci (M):** 59, 66, 74, 83, 93, 105, 120, 120+
- **Žene (F):** 47, 52, 57, 63, 69, 76, 84, 84+
