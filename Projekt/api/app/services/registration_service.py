# =============================================================
# registration_service.py — Poslovna logika za prijave
# =============================================================
# Ownership: club korisnik smije prijaviti samo liftera svog kluba.
# Admin vidi sve prijave, club vidi samo svoje.
# IntegrityError od UniqueConstraint → 409 Conflict.
# =============================================================

from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppError
from app.core.phases import Phase, get_competition_phase
from app.models.registration import Registration
from app.models.user import User
from app.repositories import competition_repo, lifter_repo, registration_repo
from app.schemas.registration import RegistrationCreate, RegistrationUpdate


async def list_registrations(
    db: AsyncSession, comp_id: int, current_user: User,
) -> list[Registration]:
    """Admin vidi sve prijave, club vidi samo prijave svojih liftera."""
    await _get_competition_or_404(db, comp_id)
    club_id = None if current_user.role == "admin" else current_user.club_id
    return await registration_repo.get_by_competition(db, comp_id, club_id=club_id)


async def get_registration(
    db: AsyncSession, comp_id: int, reg_id: int, current_user: User,
) -> Registration:
    """Dohvati prijavu s ownership provjerom."""
    reg = await registration_repo.get_by_id(db, reg_id)
    if not reg or reg.competition_id != comp_id:
        raise AppError("not_found", "Prijava nije pronađena", 404)
    _check_lifter_ownership(reg, current_user)
    return reg


async def create_registration(
    db: AsyncSession, comp_id: int, body: RegistrationCreate, current_user: User,
) -> Registration:
    """Kreiraj prijavu s ownership provjerom i duplikat zaštitom."""
    comp = await _get_competition_or_404(db, comp_id)

    phase = get_competition_phase(comp)
    if phase != Phase.OPEN:
        raise AppError("deadline_passed", "Rok za nove prijave je istekao", 400)

    lifter = await lifter_repo.get_by_id(db, body.lifter_id)
    if not lifter:
        raise AppError("not_found", "Natjecatelj nije pronađen", 404)
    if current_user.role == "club" and lifter.club_id != current_user.club_id:
        raise AppError("forbidden", "Ne možete prijaviti natjecatelja drugog kluba", 403)

    reg = Registration(
        lifter_id=body.lifter_id,
        competition_id=comp_id,
        category=body.category,
        total=body.total,
    )
    try:
        await registration_repo.create(db, reg)
    except IntegrityError:
        raise AppError(
            "duplicate",
            "Natjecatelj je već prijavljen na ovo natjecanje",
            409,
        )
    # reload da se učita lifter relacija (potrebna za RegistrationResponse)
    loaded = await registration_repo.get_by_id(db, reg.id)
    assert loaded is not None
    return loaded


async def update_registration(
    db: AsyncSession, comp_id: int, reg_id: int,
    body: RegistrationUpdate, current_user: User,
) -> Registration:
    """Ažuriraj prijavu (kategorija, total) s ownership provjerom."""
    comp = await _get_competition_or_404(db, comp_id)
    phase = get_competition_phase(comp)
    if phase == Phase.CLOSED:
        raise AppError("deadline_passed", "Izmjene nisu moguće nakon finalnog roka", 400)

    reg = await get_registration(db, comp_id, reg_id, current_user)
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(reg, field, value)
    await db.flush()
    return reg


async def withdraw_registration(
    db: AsyncSession, comp_id: int, reg_id: int, current_user: User,
) -> Registration:
    """Odjavi natjecatelja (soft delete: status → withdrawn)."""
    reg = await registration_repo.get_by_id(db, reg_id)
    if not reg or reg.competition_id != comp_id:
        raise AppError("not_found", "Prijava nije pronađena", 404)
    if reg.status == "withdrawn":
        raise AppError("already_withdrawn", "Već odjavljen", 400)

    _check_lifter_ownership(reg, current_user)

    comp = await _get_competition_or_404(db, comp_id)
    phase = get_competition_phase(comp)
    if phase == Phase.CLOSED:
        raise AppError("deadline_passed", "Izmjene nisu moguće nakon finalnog roka", 400)

    reg.status = "withdrawn"
    await db.flush()
    return reg


async def reactivate_registration(
    db: AsyncSession, comp_id: int, reg_id: int, current_user: User,
) -> Registration:
    """Ponovna aktivacija povučene prijave (dozvoljeno dok final deadline nije prošao)."""
    reg = await registration_repo.get_by_id(db, reg_id)
    if not reg or reg.competition_id != comp_id:
        raise AppError("not_found", "Prijava nije pronađena", 404)
    if reg.status == "active":
        raise AppError("already_active", "Prijava je već aktivna", 400)

    _check_lifter_ownership(reg, current_user)

    comp = await _get_competition_or_404(db, comp_id)
    phase = get_competition_phase(comp)
    if phase == Phase.CLOSED:
        raise AppError("deadline_passed", "Izmjene nisu moguće nakon finalnog roka", 400)

    reg.status = "active"
    await db.flush()
    return reg


# --- Interni helperi ---

async def _get_competition_or_404(db: AsyncSession, comp_id: int):
    comp = await competition_repo.get_by_id(db, comp_id)
    if not comp:
        raise AppError("not_found", "Natjecanje nije pronađeno", 404)
    return comp


def _check_lifter_ownership(reg: Registration, current_user: User) -> None:
    """Club korisnik smije pristupiti samo prijavama svojih liftera."""
    if current_user.role == "club" and reg.lifter.club_id != current_user.club_id:
        raise AppError("forbidden", "Ne možete pristupiti prijavama drugog kluba", 403)
