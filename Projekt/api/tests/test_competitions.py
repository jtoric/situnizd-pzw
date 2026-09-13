# =============================================================
# test_competitions.py — Testovi za /competitions endpointe
# =============================================================

from httpx import AsyncClient

from tests.conftest import auth_header


# ---- Admin CRUD ------------------------------------------------

async def test_admin_create_competition(client: AsyncClient, admin_user):
    """Admin kreira natjecanje — 201."""
    headers = await auth_header(client, "testadmin", "admin123")
    resp = await client.post(
        "/competitions/",
        json={
            "name": "Državno 2027",
            "date": "2027-06-01",
            "location": "Zagreb",
            "prelim_deadline": "2027-04-01T00:00:00Z",
            "final_deadline": "2027-05-01T00:00:00Z",
        },
        headers=headers,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["name"] == "Državno 2027"
    assert data["location"] == "Zagreb"


async def test_list_competitions(client: AsyncClient, admin_user, competition):
    """Lista natjecanja — 200."""
    headers = await auth_header(client, "testadmin", "admin123")
    resp = await client.get("/competitions/", headers=headers)
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


async def test_get_competition(client: AsyncClient, admin_user, competition):
    """Dohvat natjecanja po ID-u — 200."""
    headers = await auth_header(client, "testadmin", "admin123")
    resp = await client.get(f"/competitions/{competition.id}", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["name"] == "Test Kup"


async def test_admin_update_competition(client: AsyncClient, admin_user, competition):
    """Admin ažurira natjecanje — 200."""
    headers = await auth_header(client, "testadmin", "admin123")
    resp = await client.patch(
        f"/competitions/{competition.id}",
        json={"location": "Split"},
        headers=headers,
    )
    assert resp.status_code == 200
    assert resp.json()["location"] == "Split"


# ---- Role testovi ------------------------------------------------

async def test_club_cannot_create_competition(client: AsyncClient, club_and_user):
    """Club korisnik ne smije kreirati natjecanje (403)."""
    headers = await auth_header(client, "testclub", "klub123")
    resp = await client.post(
        "/competitions/",
        json={
            "name": "Hacker Kup",
            "date": "2027-06-01",
            "location": "Zagreb",
            "prelim_deadline": "2027-04-01T00:00:00Z",
            "final_deadline": "2027-05-01T00:00:00Z",
        },
        headers=headers,
    )
    assert resp.status_code == 403


async def test_club_cannot_update_competition(
    client: AsyncClient, club_and_user, admin_user, competition,
):
    """Club korisnik ne smije ažurirati natjecanje (403)."""
    headers = await auth_header(client, "testclub", "klub123")
    resp = await client.patch(
        f"/competitions/{competition.id}",
        json={"name": "Hakiran"},
        headers=headers,
    )
    assert resp.status_code == 403


async def test_club_can_list_competitions(
    client: AsyncClient, club_and_user, competition,
):
    """Club korisnik može vidjeti listu natjecanja."""
    headers = await auth_header(client, "testclub", "klub123")
    resp = await client.get("/competitions/", headers=headers)
    assert resp.status_code == 200


async def test_club_can_get_competition(
    client: AsyncClient, club_and_user, competition,
):
    """Club korisnik može vidjeti detalje natjecanja."""
    headers = await auth_header(client, "testclub", "klub123")
    resp = await client.get(f"/competitions/{competition.id}", headers=headers)
    assert resp.status_code == 200


# ---- Validacija ------------------------------------------------

async def test_final_deadline_before_prelim(client: AsyncClient, admin_user):
    """final_deadline <= prelim_deadline — 422."""
    headers = await auth_header(client, "testadmin", "admin123")
    resp = await client.post(
        "/competitions/",
        json={
            "name": "Bad Kup",
            "date": "2027-06-01",
            "location": "Zagreb",
            "prelim_deadline": "2027-05-01T00:00:00Z",
            "final_deadline": "2027-04-01T00:00:00Z",
        },
        headers=headers,
    )
    assert resp.status_code == 422


async def test_get_nonexistent_competition(client: AsyncClient, admin_user):
    """Dohvat nepostojećeg natjecanja — 404."""
    headers = await auth_header(client, "testadmin", "admin123")
    resp = await client.get("/competitions/9999", headers=headers)
    assert resp.status_code == 404
