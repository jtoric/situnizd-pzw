# Deploy s GitHuba na Railway

Railway direktno prati GitHub repozitorij — svaki `git push` na `main` automatski
pokreće novi deploy. Nema potrebe za GitHub Actions ni posebnim CI koracima.

---

## Preduvjet: repozitorij na GitHubu

Projekt mora biti pushnut na GitHub. Ako još nije:

```powershell
# Iz korijena projekta (gdje je .gitignore)
git init
git add .
git commit -m "initial commit"

# Kreiraj prazan repo na github.com, zatim:
git remote add origin https://github.com/<tvoje-korisnicko-ime>/<naziv-repoa>.git
git push -u origin main
```

---

## 1. Poveži Railway s GitHubom

1. Idi na [railway.app](https://railway.app) → **New Project**
2. Odaberi **"Deploy from GitHub repo"**
3. Odobri pristup GitHubu (prvi put traži autorizaciju Railway GitHub App)
4. Odaberi repozitorij iz liste

---

## 2. Dodaj PostgreSQL bazu

U projektu klikni **"+ New"** → **"Database"** → **"Add PostgreSQL"**.

Railway automatski kreira bazu i interno je dostupna ostalim servisima u projektu.

---

## 3. Konfiguriraj API servis

Railway je kreirao servis iz tvog repoa, ali ne zna gdje je Python kod.

### Root Directory

**Settings** → **Root Directory**:
```
Projekt/api
```

### Start Command

**Settings** → **Deploy** → **Start Command**:
```
uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

### Environment varijable

**Variables** tab → unesi:

| Varijabla | Vrijednost | Napomena |
|-----------|------------|----------|
| `DATABASE_URL` | Kopiraj iz PostgreSQL servisa | Zamijeni prefiks: `postgresql://` → `postgresql+asyncpg://` |
| `ENV` | `production` | Gasi Swagger docs |
| `JWT_SECRET` | Jak random string | `python -c "import secrets; print(secrets.token_urlsafe(40))"` |
| `JWT_ISSUER` | `sit-unizd` | |
| `CORS_ORIGINS` | (ostavi prazno za sada) | Dodaješ nakon koraka 5 |

### Migracije i seed (jednom)

Nakon što se API uspješno deploya, otvori **Railway Shell**
(ikona terminala u gornjem desnom kutu servisa):

```bash
alembic upgrade head
python -m app.seed
```

Seed kreira: `admin` / `admin123`, `behemot` / `klub123`, `heraklo` / `klub123`.

> **Promjena lozinki nakon seeda:** Lozinke klubova mijenja admin via
> `POST /clubs/{club_id}/reset-password` s tijelom `{"new_password": "..."}`.
> Admin lozinku trenutno nema dedicated endpoint — promijeni direktno u bazi:
> ```bash
> # u Railway Shell-u
> python -c "
> import asyncio, bcrypt
> from app.core.database import AsyncSessionLocal
> from app.models.user import User
> from sqlalchemy import select, update
> hash = bcrypt.hashpw(b'nova-lozinka', bcrypt.gensalt()).decode()
> async def run():
>     async with AsyncSessionLocal() as db:
>         await db.execute(update(User).where(User.username=='admin').values(hashed_password=hash))
>         await db.commit()
> asyncio.run(run())
> "
> ```

---

## 4. Konfiguriraj Web servis

Klikni **"+ New"** → **"GitHub Repo"** → isti repozitorij (drugi servis iz istog repo).

### Root Directory

**Settings** → **Root Directory**:
```
Projekt/web
```

### Build & Deploy

**Settings** → **Deploy**:

| Polje | Vrijednost |
|-------|------------|
| **Build Command** | `npm ci && npm run build` |
| **Start Command** | (prazno) |
| **Publish Directory** | `dist` |

> Ako Railway ne ponudi "Publish Directory", idi na **Settings** → **Build** →
> postavi tip na **Static**.

### Environment varijable

| Varijabla | Vrijednost |
|-----------|------------|
| `VITE_API_URL` | URL API servisa, npr. `https://api-xyz.up.railway.app` |

> `VITE_` prefiks je obavezan — bez njega Vite ne ubacuje varijablu u bundle.  
> Nakon promjene ove varijable **obavezno** ručno pokreni novi build
> (**Deployments** → **Deploy Now**) jer je build-time varijabla.

---

## 5. Poveži CORS

Sad znaš URL web servisa. Idi na **API servis** → **Variables** → postavi:

```
CORS_ORIGINS=https://web-xyz.up.railway.app
```

Railway automatski restarta API.

---

## 6. Automatski deploy pri svakom pushu

Od sada vrijedi:

```
git push origin main
    ↓
GitHub obavijesti Railway
    ↓
Railway build + deploy (API i Web paralelno)
```

Nema ručnih koraka. Build log možeš pratiti u **Deployments** tabu u realnom vremenu.

### Samo određene grane (opcionalno)

Ako ne želiš da svaki push na `main` deploya (npr. radiš na feature granama):

**Settings** → **Deploy** → **Branch** → promijeni s `main` na `production`
ili bilo koju drugu granu koja ti služi kao deploy branch.

---

## 7. Provjera nakon deploya

```powershell
# Zamijeni s tvojim URL-ovima
$api = "https://api-xyz.up.railway.app"
$web = "https://web-xyz.up.railway.app"

# Health check
Invoke-RestMethod "$api/health"
# → { "status": "ok" }

# CORS provjera
Invoke-WebRequest -Method OPTIONS "$api/auth/login" `
  -Headers @{ "Origin" = $web; "Access-Control-Request-Method" = "POST" } `
  -UseBasicParsing | Select-Object -ExpandProperty Headers
# → Access-Control-Allow-Origin: https://web-xyz.up.railway.app
```

---

## 8. Česti problemi

### Railway ne detektira Python (Railpack greška)

Uzrok je gotovo uvijek krivi **Root Directory**. Railpack mora vidjeti
`requirements.txt` u korijenu direktorija koji builda.  
Provjeri: **Settings** → **Root Directory** = `Projekt/api`.

### Build web-a prolazi lokalno ali pada na Railway

Najčešći uzrok: `VITE_API_URL` nije postavljen prije build-a.  
Railway build-time varijable moraju biti postavljene **prije** pokretanja builda.  
Provjeri **Variables** tab i pokreni novi deploy.

### `postgresql://` vs `postgresql+asyncpg://`

Railway PostgreSQL plugin daje URL oblika `postgresql://...`.  
SQLAlchemy asyncpg driver treba `postgresql+asyncpg://...`.  
Kopiraj URL iz PostgreSQL servisa u API **Variables** i ručno promijeni prefiks.

### Promjena env varijable ne efektira web

`VITE_API_URL` je **build-time** varijabla — ugrađuje se u JavaScript bundle pri buildu.  
Sama promjena varijable ne mijenja već deployani bundle.  
Nakon promjene: **Deployments** → **Deploy Now** → Railway ponovo builda.

### Migracije treba ponoviti (nova tablica, nova kolona)

Svaki put kad dodaš Alembic migraciju i pushaš na main:

1. Railway automatski deploya novi kod
2. Ti ručno otvoriš Railway Shell i pokreneš `alembic upgrade head`

Alembic migracije se **ne pokreću automatski** — Railway ne zna za njih.

---

## 9. Produkcijski checklist

- [ ] Root Directory za API servis postavljen na `Projekt/api`
- [ ] Root Directory za Web servis postavljen na `Projekt/web`
- [ ] `DATABASE_URL` ima prefiks `postgresql+asyncpg://`
- [ ] `JWT_SECRET` nije `change-me-in-production`
- [ ] `ENV=production` (Swagger na `/docs` nedostupan)
- [ ] `alembic upgrade head` pokrenut u Railway Shell-u
- [ ] `python -m app.seed` pokrenut — admin i klubovi postoje
- [ ] `CORS_ORIGINS` sadrži točan URL web servisa (bez trailing `/`)
- [ ] `VITE_API_URL` u web servisu sadrži točan URL API servisa
- [ ] Web rebuild pokrenut nakon postavljanja `VITE_API_URL`
- [ ] `GET /health` vraća `{ "status": "ok" }`
- [ ] Login flow radi end-to-end: prijava → dashboard → logout
- [ ] HTTPS aktivan (Railway daje automatski za `*.up.railway.app`)
