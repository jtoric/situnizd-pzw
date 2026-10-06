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

## **Predavanje 7 — Frontend: arhitektura SPA \+ router \+ layout**

1. `feat(web): scaffold typescript app with layout, router, and navigation shell`

2. `feat(web): add route structure for admin and club areas`

3. `chore(web): add eslint/prettier and basic project conventions`

4. `docs: add frontend structure and component guidelines`

---

## **Predavanje 8 — Frontend: API komunikacija \+ auth flow (JWT) \+ guards**

1. `feat(web): add API client wrapper with base URL and interceptors`

2. `feat(web): implement auth store (Pinia) and login page`

3. `feat(web): add route guards for role-based access (admin/club)`

4. `feat(web): implement token refresh flow and 401 handling`

5. `fix(web): add global error handling and toast/alert pattern`

---

## **Predavanje 9 — Frontend: state management \+ UX discipline (lifters \+ prijave)**

1. `feat(web): add lifters list view with loading/error/empty states`

2. `feat(web): add lifter create/edit form with validation`

3. `feat(web): add competitions list and registration form`

4. `feat(web): add my registrations view with status badges`

5. `refactor(web): extract reusable form and table components`

---

## **Predavanje 10 — Frontend: kompleksne tablice (admin) \+ filter/pagination \+ permission-aware UI**

1. `feat(web): add admin competitions CRUD screens`

2. `feat(web): add admin registrations table with filters and pagination`

3. `feat(web): add approve/reject UI with modal and reason`

4. `feat(web): add CSV export button and download flow`

5. `fix(web): disable actions based on competition phase (prelim/final/locked)`

---

## **Predavanje 11 — Testiranje full-stack aplikacije**

1. `test(api): add conftest with async client and db fixtures`

2. `test(api): add coverage config and fill gaps in rule tests`

3. `test(web): add vitest setup with util and store unit tests`

4. `test(web): add component tests for form field`

5. `test(e2e): add playwright login and phase rule tests`

---

## **Predavanje 12 — Frontend: production \+ deploy \+ polish**

1. `chore: configure production env and CORS settings for deployment`

2. `feat(web): add build-time env config and runtime API base handling`

3. `ci: add pipeline for lint/test/build (api + web)`

4. `docs: add deploy guide (Railway) and production checklist`

5. `refactor: final cleanup, remove dead code, tighten types and validation`

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
