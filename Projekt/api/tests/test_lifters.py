# =============================================================
# test_lifters.py — Testovi za /clubs/{club_id}/lifters endpointe
# =============================================================

from httpx import AsyncClient

from tests.conftest import auth_header


# ---- CRUD happy path ------------------------------------------------

async def test_create_lifter(client: AsyncClient, club_and_user):
    """Club kreira natjecatelja — 201."""
    club, _ = club_and_user
    headers = await auth_header(client, "testclub", "klub123")
    resp = await client.post(
        f"/clubs/{club.id}/lifters/",
        json={
            "first_name": "Marko",
            "last_name": "Markić",
            "birth_date": "2000-01-15",
            "gender": "M",
        },
        headers=headers,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["first_name"] == "Marko"
    assert data["club_id"] == club.id


async def test_list_lifters(client: AsyncClient, club_and_user, lifter):
    """Lista natjecatelja vraća 200."""
    club, _ = club_and_user
    headers = await auth_header(client, "testclub", "klub123")
    resp = await client.get(f"/clubs/{club.id}/lifters/", headers=headers)

    assert resp.status_code == 200
    data = resp.json()
    assert len(data) >= 1


async def test_get_lifter(client: AsyncClient, club_and_user, lifter):
    """Dohvat natjecatelja po ID-u — 200."""
    club, _ = club_and_user
    headers = await auth_header(client, "testclub", "klub123")
    resp = await client.get(
        f"/clubs/{club.id}/lifters/{lifter.id}", headers=headers,
    )
    assert resp.status_code == 200
    assert resp.json()["first_name"] == "Marko"


async def test_update_lifter(client: AsyncClient, club_and_user, lifter):
    """Parcijalni update natjecatelja — 200."""
    club, _ = club_and_user
    headers = await auth_header(client, "testclub", "klub123")
    resp = await client.patch(
        f"/clubs/{club.id}/lifters/{lifter.id}",
        json={"last_name": "Novak"},
        headers=headers,
    )
    assert resp.status_code == 200
    assert resp.json()["last_name"] == "Novak"


async def test_delete_lifter(client: AsyncClient, club_and_user, lifter):
    """Brisanje natjecatelja — 204."""
    club, _ = club_and_user
    headers = await auth_header(client, "testclub", "klub123")
    resp = await client.delete(
        f"/clubs/{club.id}/lifters/{lifter.id}", headers=headers,
    )
    assert resp.status_code == 204


# ---- Ownership testovi ------------------------------------------------

async def test_club_cannot_access_other_clubs_lifters(
    client: AsyncClient, club_and_user, club_b_and_user, lifter,
):
    """Club ne smije vidjeti natjecatelje drugog kluba (403)."""
    club, _ = club_and_user
    headers = await auth_header(client, "rivalclub", "rival123")
    resp = await client.get(
        f"/clubs/{club.id}/lifters/", headers=headers,
    )
    assert resp.status_code == 403


async def test_club_cannot_create_lifter_in_other_club(
    client: AsyncClient, club_and_user, club_b_and_user,
):
    """Club ne smije dodati natjecatelja u drugi klub (403)."""
    club, _ = club_and_user
    headers = await auth_header(client, "rivalclub", "rival123")
    resp = await client.post(
        f"/clubs/{club.id}/lifters/",
        json={
            "first_name": "Ana",
            "last_name": "Anić",
            "birth_date": "1995-05-01",
            "gender": "F",
        },
        headers=headers,
    )
    assert resp.status_code == 403


async def test_admin_can_access_any_clubs_lifters(
    client: AsyncClient, admin_user, club_and_user, lifter,
):
    """Admin može vidjeti natjecatelje bilo kojeg kluba."""
    club, _ = club_and_user
    headers = await auth_header(client, "testadmin", "admin123")
    resp = await client.get(f"/clubs/{club.id}/lifters/", headers=headers)
    assert resp.status_code == 200


# ---- Validacija ------------------------------------------------

async def test_create_lifter_future_birthdate(client: AsyncClient, club_and_user):
    """Datum rođenja u budućnosti — 422."""
    club, _ = club_and_user
    headers = await auth_header(client, "testclub", "klub123")
    resp = await client.post(
        f"/clubs/{club.id}/lifters/",
        json={
            "first_name": "Future",
            "last_name": "Person",
            "birth_date": "2099-01-01",
            "gender": "M",
        },
        headers=headers,
    )
    assert resp.status_code == 422


async def test_create_lifter_invalid_gender(client: AsyncClient, club_and_user):
    """Nevaljan spol (nije M/F) — 422."""
    club, _ = club_and_user
    headers = await auth_header(client, "testclub", "klub123")
    resp = await client.post(
        f"/clubs/{club.id}/lifters/",
        json={
            "first_name": "Test",
            "last_name": "Test",
            "birth_date": "2000-01-01",
            "gender": "X",
        },
        headers=headers,
    )
    assert resp.status_code == 422


# ---- Paginacija ------------------------------------------------

async def test_list_lifters_pagination(client: AsyncClient, club_and_user):
    """Paginacija limit/offset radi."""
    club, _ = club_and_user
    headers = await auth_header(client, "testclub", "klub123")

    for i in range(3):
        await client.post(
            f"/clubs/{club.id}/lifters/",
            json={
                "first_name": f"Lifter{i}",
                "last_name": "Test",
                "birth_date": "2000-01-01",
                "gender": "M",
            },
            headers=headers,
        )

    resp = await client.get(
        f"/clubs/{club.id}/lifters/?limit=2&offset=0", headers=headers,
    )
    assert resp.status_code == 200
    assert len(resp.json()) == 2

    resp2 = await client.get(
        f"/clubs/{club.id}/lifters/?limit=2&offset=2", headers=headers,
    )
    assert resp2.status_code == 200
    assert len(resp2.json()) == 1


async def test_get_nonexistent_lifter(client: AsyncClient, club_and_user):
    """Dohvat nepostojećeg natjecatelja — 404."""
    club, _ = club_and_user
    headers = await auth_header(client, "testclub", "klub123")
    resp = await client.get(
        f"/clubs/{club.id}/lifters/9999", headers=headers,
    )
    assert resp.status_code == 404
