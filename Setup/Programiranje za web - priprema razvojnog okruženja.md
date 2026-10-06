# Programiranje za web - priprema razvojnog okruženja

28. rujna 2026. · Josip Torić

## Uvod

Do prvog predavanja 8. listopada 2026. na svom računalu instalirajte sve alate s popisa i pokrenite radni primjer iz mape `pzw-provjera`. Ako svaka naredba ispiše ono što je navedeno, okruženje je spremno za cijeli kolegij.

Ako nešto ne radi, pogledajte odjeljak *Česti problemi* na kraju uputa. Ako to ne pomogne, javite se asistentu Josipu Toriću (jtoric@unizd.hr) <u>prije prvog predavanja</u> kako bismo osigurali neometan početak nastave.

## Popis softvera

Instalirajte šest alata i ekstenzije iz tablice, svaki prema službenim uputama za svoj operacijski sustav. Nakon svake instalacije zatvorite i ponovno otvorite terminal, odnosno cijeli VS Code, da se osvježi PATH.

| Alat | Verzija | Za što služi | Upute za instalaciju |
| --- | --- | --- | --- |
| Git | najnovija | verzioniranje koda i predaja projekta | [git-scm.com/downloads](https://git-scm.com/downloads) |
| Python | 3.11 ili novija, preporuka 3.13 | backend u FastAPI-ju | [python.org/downloads](https://www.python.org/downloads/) |
| uv | najnovija | virtualna okruženja i paketi | [docs.astral.sh/uv](https://docs.astral.sh/uv/getting-started/installation/) |
| Docker Desktop | najnovija | PostgreSQL baza u kontejneru, uključuje Docker Compose | [docs.docker.com/desktop](https://docs.docker.com/desktop/) |
| Node.js | 24 LTS, minimalno 22.18 | frontend: Vue, Vite i TypeScript | [nodejs.org/download](https://nodejs.org/en/download) |
| VS Code | najnovija | editor | [code.visualstudio.com](https://code.visualstudio.com/download) |
| Ekstenzije za VS Code | najnovije | Python (Microsoft), Vue - Official, SQLTools + PostgreSQL driver | Extensions panel u VS Code-u, prečac Ctrl+Shift+X |

Napomene:

- **Windows:** u Python installeru označite *Add python.exe to PATH*. Docker Desktop traži WSL 2. Installer ga obično nudi sam, a ako ne, slijedite [upute za WSL](https://learn.microsoft.com/windows/wsl/install).
- **macOS:** sve osim Docker Desktopa možete instalirati kroz Homebrew: `brew install git python uv node`.
- **Linux:** umjesto Docker Desktopa dovoljni su [Docker Engine i Compose plugin](https://docs.docker.com/engine/install/). Korisnika dodajte u grupu `docker`.

Nakon instalacije Gita jednom postavite ime i e-mail. Koristite isti e-mail kao na GitHubu:

```bash
git config --global user.name "Ime Prezime"
git config --global user.email "vas.email@example.com"
```

### Provjera verzija

U bilo kojem terminalu:

| Naredba | Očekivani ispis |
| --- | --- |
| `git --version` | `git version 2.x` |
| `python --version`, na macOS-u i Linuxu `python3 --version` | `Python 3.11` ili novija |
| `uv --version` | `uv 0.x.y` |
| `docker --version` | `Docker version 2x.y.z` |
| `docker compose version` | `Docker Compose version v2.x` ili novija |
| `node --version` | `v24.x` ili `v22.18` i novija |
| `npm --version` | `10.x` ili novija |
| `code --version` | broj verzije VS Code-a |

Brojevi verzija smiju biti i veći od navedenih.

## Radni primjer

Radni primjer se nalazi u mapi `pzw-provjera` i sadrži iste slojeve koje ćemo graditi kroz semestar:

```text
pzw-provjera/
  docker-compose.yml    # PostgreSQL baza u Dockeru
  api/                  # FastAPI backend koji čita iz baze
  web/                  # Vue + TypeScript frontend
```

Mapu otvorite u VS Code-u (*File → Open Folder*), a naredbe pokrećite u njegovu terminalu (*Terminal → New Terminal*).

### 1. Baza

Pokrenite Docker Desktop i pričekajte da u izborniku piše *Engine running*. U mapi `pzw-provjera`:

```bash
docker compose up -d db
docker compose ps
```

Prvo pokretanje preuzima *image* od oko 150 MB pa traje minutu-dvije. Očekivani ispis druge naredbe je red s `db` u kojem piše `Up` i `0.0.0.0:5432->5432/tcp`, na primjer:

```text
NAME                IMAGE         COMMAND                  SERVICE   CREATED         STATUS         PORTS
pzw-provjera-db-1   postgres:17   "docker-entrypoint.s…"   db        7 seconds ago   Up 6 seconds   0.0.0.0:5432->5432/tcp, [::]:5432->5432/tcp
```

### 2. Backend

```bash
cd api
uv venv

# aktivacija - Windows (PowerShell)
.venv\Scripts\Activate.ps1
# aktivacija - macOS / Linux
source .venv/bin/activate

uv pip install -r requirements.txt
uvicorn main:app --reload
```

Nakon zadnje naredbe očekivani ispis je:

```text
INFO:     Will watch for changes in these directories: ['...\\pzw-provjera\\api']
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [9296] using WatchFiles
INFO:     Started server process [16616]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

Brojevi procesa u uglatim zagradama razlikovat će se kod vas. U pregledniku otvorite:

| Adresa | Očekivani ispis |
| --- | --- |
| <http://127.0.0.1:8000/health> | `{"status":"ok","database":"PostgreSQL 17..."}` |
| <http://127.0.0.1:8000/docs> | Swagger UI s endpointom `GET /health` |

Server ostavite da radi, a za sljedeći korak otvorite novi terminal gumbom **+** u panelu terminala.

### 3. Frontend

Iz mape `pzw-provjera`:

```bash
cd web
npm install
npm run type-check
npm run dev
```

`npm run type-check` ne smije ispisati nijednu grešku. Nakon `npm run dev` otvorite <http://localhost:5173>. Očekivani ispis je Vue stranica s naslovom **You did it!**

### Završetak

Po uspješnoj provjeri okruženja zaustavite oba servera s Ctrl+C u njihovim terminalima i ugasite bazu naredbom `docker compose down` u mapi `pzw-provjera`. Na predavanjima ćemo krenuti graditi projekt iznova.

## Česti problemi

Prije svega zatvorite i ponovno otvorite terminal, odnosno cijeli VS Code. Ako to ne pomogne, ponovno pokrenite računalo.

| Simptom | Uzrok | Rješenje |
| --- | --- | --- |
| `python` nije prepoznat ili otvara Microsoft Store na Windowsima | Python nije u PATH-u | Ponovno pokrenite installer i označite *Add python.exe to PATH*; u *Settings → Apps → Advanced app settings → App execution aliases* isključite aliase za `python.exe` |
| `Activate.ps1 cannot be loaded because running scripts is disabled` | PowerShell blokira skripte | Jednom pokrenite `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `uvicorn` nije prepoznat | Virtualno okruženje nije aktivirano | Aktivirajte ga; ispred prompta mora pisati `(api)` ili `(.venv)`. Alternativa bez aktivacije: `uv run uvicorn main:app --reload` |
| `failed to connect to the docker API` ili `Cannot connect to the Docker daemon` | Docker Desktop nije pokrenut | Pokrenite ga i pričekajte *Engine running* |
| `WSL 2 installation is incomplete` ili greška o virtualizaciji | Nedostaje WSL 2 ili je virtualizacija isključena | U PowerShellu kao administrator pokrenite `wsl --install`; ako ne pomogne, uključite virtualizaciju VT-x ili AMD-V u BIOS-u |
| `Bind for 0.0.0.0:5432 failed: port is already allocated` | Port 5432 drži lokalni PostgreSQL ili drugi kontejner | `docker ps` pokaže kontejner koji treba zaustaviti; inače u `docker-compose.yml` stavite `"5433:5432"`, a u `api/main.py` `localhost:5433` |
| `/health` vraća 500, u terminalu `ConnectionRefusedError` | Baza nije pokrenuta ili se još diže | `docker compose ps`; pričekajte nekoliko sekundi i osvježite |
| `npm` ili `node` nije prepoznat | Node.js nije instaliran ili je VS Code otvoren prije instalacije | Instalirajte Node.js, pa potpuno zatvorite i ponovno otvorite VS Code; terminal u VS Code-u vidi novi PATH tek nakon toga |
| `npm install` javlja `Unsupported engine` | Prestara verzija Node.js-a | Instalirajte Node.js 24 LTS |
| `code` nije prepoznat na macOS-u | VS Code nije dodan u PATH | U VS Code-u: Command Palette → *Shell Command: Install 'code' command in PATH* |
