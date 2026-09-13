# =============================================================
# test_registrations.py — Testovi za registration endpointe
# =============================================================

from freezegun import freeze_time
from httpx import AsyncClient

from tests.conftest import auth_header

# Rokovi competition fixture-a:
#   prelim_deadline = 2026-04-15
#   final_deadline  = 2026-05-01
#
# Faze:
#   OPEN           — prije 2026-04-15  (koristimo 2026-04-01)
#   PRELIM_PASSED  — između rokova     (koristimo 2026-04-20)
#   CLOSED         — nakon 2026-05-01  (koristimo 2026-05-10)


# ---- CRUD happy path ------------------------------------------------

@freeze_time("2026-04-01 10:00:00")
async def test_create_registration(
    client: AsyncClient, club_and_user, lifter, competition,
):
    """Club prijavljuje natjecatelja na natjecanje — 201."""
    headers = await auth_header(client, "testclub", "klub123")
    resp = await client.post(
        f"/competitions/{competition.id}/registrations/",
        json={
            "lifter_id": lifter.id,
            "category": "93",
            "total": 500,
        },
        headers=headers,
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["lifter_id"] == lifter.id
    assert data["competition_id"] == competition.id
    assert data["category"] == "93"
    assert data["status"] == "active"


@freeze_time("2026-04-01 10:00:00")
async def test_list_registrations(
    client: AsyncClient, club_and_user, lifter, competition,
):
    """Lista prijava za natjecanje — 200."""
    headers = await auth_header(client, "testclub", "klub123")
    await client.post(
        f"/competitions/{competition.id}/registrations/",
        json={"lifter_id": lifter.id, "category": "93", "total": 500},
        headers=headers,
    )
    resp = await client.get(
        f"/competitions/{competition.id}/registrations/", headers=headers,
    )
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


@freeze_time("2026-04-01 10:00:00")
async def test_get_registration(
    client: AsyncClient, club_and_user, lifter, competition,
):
    """Dohvat prijave po ID-u — 200."""
    headers = await auth_header(client, "testclub", "klub123")
    create_resp = await client.post(
        f"/competitions/{competition.id}/registrations/",
        json={"lifter_id": lifter.id, "category": "93", "total": 500},
        headers=headers,
    )
    reg_id = create_resp.json()["id"]
    resp = await client.get(
        f"/competitions/{competition.id}/registrations/{reg_id}",
        headers=headers,
    )
    assert resp.status_code == 200
    assert resp.json()["category"] == "93"


@freeze_time("2026-04-01 10:00:00")
async def test_update_registration(
    client: AsyncClient, club_and_user, lifter, competition,
):
    """Promjena kategorije prijave — 200."""
    headers = await auth_header(client, "testclub", "klub123")
    create_resp = await client.post(
        f"/competitions/{competition.id}/registrations/",
        json={"lifter_id": lifter.id, "category": "93", "total": 500},
        headers=headers,
    )
    reg_id = create_resp.json()["id"]
    resp = await client.patch(
        f"/competitions/{competition.id}/registrations/{reg_id}",
        json={"category": "105"},
        headers=headers,
    )
    assert resp.status_code == 200
    assert resp.json()["category"] == "105"


# ---- Duplikat ------------------------------------------------

@freeze_time("2026-04-01 10:00:00")
async def test_duplicate_registration(
    client: AsyncClient, club_and_user, lifter, competition,
):
    """Dupla prijava istog natjecatelja — 409."""
    headers = await auth_header(client, "testclub", "klub123")
    await client.post(
        f"/competitions/{competition.id}/registrations/",
        json={"lifter_id": lifter.id, "category": "93", "total": 500},
        headers=headers,
    )
    resp = await client.post(
        f"/competitions/{competition.id}/registrations/",
        json={"lifter_id": lifter.id, "category": "105", "total": 400},
        headers=headers,
    )
    assert resp.status_code == 409
    assert resp.json()["code"] == "duplicate"


# ---- Validacija ------------------------------------------------

@freeze_time("2026-04-01 10:00:00")
async def test_invalid_category(
    client: AsyncClient, club_and_user, lifter, competition,
):
    """Nepoznata kategorija — 422."""
    headers = await auth_header(client, "testclub", "klub123")
    resp = await client.post(
        f"/competitions/{competition.id}/registrations/",
        json={"lifter_id": lifter.id, "category": "999", "total": 500},
        headers=headers,
    )
    assert resp.status_code == 422


@freeze_time("2026-04-01 10:00:00")
async def test_nonexistent_lifter(
    client: AsyncClient, club_and_user, competition,
):
    """Prijava nepostojećeg natjecatelja — 404."""
    headers = await auth_header(client, "testclub", "klub123")
    resp = await client.post(
        f"/competitions/{competition.id}/registrations/",
        json={"lifter_id": 9999, "category": "93", "total": 0},
        headers=headers,
    )
    assert resp.status_code == 404


async def test_nonexistent_competition(
    client: AsyncClient, club_and_user, lifter,
):
    """Prijava na nepostojeće natjecanje — 404."""
    headers = await auth_header(client, "testclub", "klub123")
    resp = await client.post(
        "/competitions/9999/registrations/",
        json={"lifter_id": lifter.id, "category": "93", "total": 0},
        headers=headers,
    )
    assert resp.status_code == 404


# ---- Ownership ------------------------------------------------

@freeze_time("2026-04-01 10:00:00")
async def test_club_cannot_register_other_clubs_lifter(
    client: AsyncClient, club_and_user, club_b_and_user, lifter, competition,
):
    """Club ne smije prijaviti natjecatelja drugog kluba (403)."""
    headers = await auth_header(client, "rivalclub", "rival123")
    resp = await client.post(
        f"/competitions/{competition.id}/registrations/",
        json={"lifter_id": lifter.id, "category": "93", "total": 500},
        headers=headers,
    )
    assert resp.status_code == 403


@freeze_time("2026-04-01 10:00:00")
async def test_club_sees_only_own_registrations(
    client: AsyncClient, admin_user, club_and_user, club_b_and_user,
    lifter, competition, db,
):
    """Club u listi vidi samo prijave svojih natjecatelja."""
    headers_a = await auth_header(client, "testclub", "klub123")
    await client.post(
        f"/competitions/{competition.id}/registrations/",
        json={"lifter_id": lifter.id, "category": "93", "total": 500},
        headers=headers_a,
    )

    headers_b = await auth_header(client, "rivalclub", "rival123")
    resp = await client.get(
        f"/competitions/{competition.id}/registrations/",
        headers=headers_b,
    )
    assert resp.status_code == 200
    assert len(resp.json()) == 0


@freeze_time("2026-04-01 10:00:00")
async def test_admin_sees_all_registrations(
    client: AsyncClient, admin_user, club_and_user, lifter, competition,
):
    """Admin vidi sve prijave."""
    headers_club = await auth_header(client, "testclub", "klub123")
    await client.post(
        f"/competitions/{competition.id}/registrations/",
        json={"lifter_id": lifter.id, "category": "93", "total": 500},
        headers=headers_club,
    )

    headers_admin = await auth_header(client, "testadmin", "admin123")
    resp = await client.get(
        f"/competitions/{competition.id}/registrations/",
        headers=headers_admin,
    )
    assert resp.status_code == 200
    assert len(resp.json()) >= 1


# ---- Faze natjecanja ------------------------------------------------

@freeze_time("2026-04-01 10:00:00")
async def test_create_registration_open_phase(
    client: AsyncClient, club_and_user, lifter, competition,
):
    """Prijava u OPEN fazi — 201."""
    headers = await auth_header(client, "testclub", "klub123")
    resp = await client.post(
        f"/competitions/{competition.id}/registrations/",
        json={"lifter_id": lifter.id, "category": "83", "total": 500},
        headers=headers,
    )
    assert resp.status_code == 201


@freeze_time("2026-04-20 10:00:00")
async def test_create_registration_prelim_passed(
    client: AsyncClient, club_and_user, lifter, competition,
):
    """Prijava nakon prelim roka — 400 deadline_passed."""
    headers = await auth_header(client, "testclub", "klub123")
    resp = await client.post(
        f"/competitions/{competition.id}/registrations/",
        json={"lifter_id": lifter.id, "category": "83", "total": 500},
        headers=headers,
    )
    assert resp.status_code == 400
    assert resp.json()["code"] == "deadline_passed"


@freeze_time("2026-05-10 10:00:00")
async def test_create_registration_closed(
    client: AsyncClient, club_and_user, lifter, competition,
):
    """Prijava nakon final roka — 400 deadline_passed."""
    headers = await auth_header(client, "testclub", "klub123")
    resp = await client.post(
        f"/competitions/{competition.id}/registrations/",
        json={"lifter_id": lifter.id, "category": "83", "total": 500},
        headers=headers,
    )
    assert resp.status_code == 400
    assert resp.json()["code"] == "deadline_passed"


@freeze_time("2026-04-20 10:00:00")
async def test_update_category_prelim_passed(
    client: AsyncClient, club_and_user, lifter, competition, db,
):
    """Promjena kategorije u PRELIM_PASSED fazi — 200 (dozvoljeno)."""
    from app.models.registration import Registration
    reg = Registration(
        lifter_id=lifter.id, competition_id=competition.id,
        category="93", total=500,
    )
    db.add(reg)
    await db.commit()
    await db.refresh(reg)

    headers = await auth_header(client, "testclub", "klub123")
    resp = await client.patch(
        f"/competitions/{competition.id}/registrations/{reg.id}",
        json={"category": "105"},
        headers=headers,
    )
    assert resp.status_code == 200
    assert resp.json()["category"] == "105"


@freeze_time("2026-05-10 10:00:00")
async def test_update_category_closed(
    client: AsyncClient, club_and_user, lifter, competition, db,
):
    """Promjena kategorije u CLOSED fazi — 400 deadline_passed."""
    from app.models.registration import Registration
    reg = Registration(
        lifter_id=lifter.id, competition_id=competition.id,
        category="93", total=500,
    )
    db.add(reg)
    await db.commit()
    await db.refresh(reg)

    headers = await auth_header(client, "testclub", "klub123")
    resp = await client.patch(
        f"/competitions/{competition.id}/registrations/{reg.id}",
        json={"category": "105"},
        headers=headers,
    )
    assert resp.status_code == 400
    assert resp.json()["code"] == "deadline_passed"


# ---- Odjava (withdraw) ------------------------------------------------

@freeze_time("2026-04-01 10:00:00")
async def test_withdraw_open(
    client: AsyncClient, club_and_user, lifter, competition,
):
    """Odjava u OPEN fazi — 200, status withdrawn."""
    headers = await auth_header(client, "testclub", "klub123")
    create_resp = await client.post(
        f"/competitions/{competition.id}/registrations/",
        json={"lifter_id": lifter.id, "category": "93", "total": 500},
        headers=headers,
    )
    reg_id = create_resp.json()["id"]

    resp = await client.post(
        f"/competitions/{competition.id}/registrations/{reg_id}/withdraw",
        headers=headers,
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "withdrawn"


@freeze_time("2026-04-20 10:00:00")
async def test_withdraw_prelim_passed(
    client: AsyncClient, club_and_user, lifter, competition, db,
):
    """Odjava u PRELIM_PASSED fazi — 200 (dozvoljeno)."""
    from app.models.registration import Registration
    reg = Registration(
        lifter_id=lifter.id, competition_id=competition.id,
        category="93", total=500,
    )
    db.add(reg)
    await db.commit()
    await db.refresh(reg)

    headers = await auth_header(client, "testclub", "klub123")
    resp = await client.post(
        f"/competitions/{competition.id}/registrations/{reg.id}/withdraw",
        headers=headers,
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "withdrawn"


@freeze_time("2026-05-10 10:00:00")
async def test_withdraw_closed(
    client: AsyncClient, club_and_user, lifter, competition, db,
):
    """Odjava u CLOSED fazi — 400 deadline_passed."""
    from app.models.registration import Registration
    reg = Registration(
        lifter_id=lifter.id, competition_id=competition.id,
        category="93", total=500,
    )
    db.add(reg)
    await db.commit()
    await db.refresh(reg)

    headers = await auth_header(client, "testclub", "klub123")
    resp = await client.post(
        f"/competitions/{competition.id}/registrations/{reg.id}/withdraw",
        headers=headers,
    )
    assert resp.status_code == 400
    assert resp.json()["code"] == "deadline_passed"


@freeze_time("2026-04-01 10:00:00")
async def test_withdraw_already_withdrawn(
    client: AsyncClient, club_and_user, lifter, competition,
):
    """Ponovna odjava već odjavljenog — 400 already_withdrawn."""
    headers = await auth_header(client, "testclub", "klub123")
    create_resp = await client.post(
        f"/competitions/{competition.id}/registrations/",
        json={"lifter_id": lifter.id, "category": "93", "total": 500},
        headers=headers,
    )
    reg_id = create_resp.json()["id"]

    await client.post(
        f"/competitions/{competition.id}/registrations/{reg_id}/withdraw",
        headers=headers,
    )
    resp = await client.post(
        f"/competitions/{competition.id}/registrations/{reg_id}/withdraw",
        headers=headers,
    )
    assert resp.status_code == 400
    assert resp.json()["code"] == "already_withdrawn"


@freeze_time("2026-04-01 10:00:00")
async def test_withdraw_other_clubs_registration(
    client: AsyncClient, club_and_user, club_b_and_user, lifter, competition,
):
    """Club ne smije odjaviti natjecatelja drugog kluba — 403."""
    headers_a = await auth_header(client, "testclub", "klub123")
    create_resp = await client.post(
        f"/competitions/{competition.id}/registrations/",
        json={"lifter_id": lifter.id, "category": "93", "total": 500},
        headers=headers_a,
    )
    reg_id = create_resp.json()["id"]

    headers_b = await auth_header(client, "rivalclub", "rival123")
    resp = await client.post(
        f"/competitions/{competition.id}/registrations/{reg_id}/withdraw",
        headers=headers_b,
    )
    assert resp.status_code == 403
