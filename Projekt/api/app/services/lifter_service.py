# =============================================================
# lifter_service.py — Poslovna logika za natjecatelje
# =============================================================

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppError
from app.models.lifter import Lifter
from app.models.user import User
from app.repositories import lifter_repo
from app.schemas.lifter import LifterCreate, LifterUpdate


def _check_club_access(current_user: User, club_id: int) -> None:
    """Club korisnik smije pristupiti samo natjecateljima svog kluba."""
    if current_user.role == "club" and current_user.club_id != club_id:
        raise AppError("forbidden", "Ne možete pristupiti natjecateljima drugog kluba", 403)


async def list_lifters(
    db: AsyncSession,
    club_id: int,
    current_user: User,
    gender: str | None = None,
    limit: int = 20,
    offset: int = 0,
) -> list[Lifter]:
    """Lista natjecatelja kluba s ownership provjerom."""
    _check_club_access(current_user, club_id)
    return await lifter_repo.get_by_club(db, club_id, gender=gender, limit=limit, offset=offset)


async def get_lifter(
    db: AsyncSession, club_id: int, lifter_id: int, current_user: User,
) -> Lifter:
    """Dohvati natjecatelja s ownership provjerom."""
    _check_club_access(current_user, club_id)
    lifter = await lifter_repo.get_by_id(db, lifter_id)
    if not lifter or lifter.club_id != club_id:
        raise AppError("not_found", "Natjecatelj nije pronađen", 404)
    return lifter


async def create_lifter(
    db: AsyncSession, club_id: int, body: LifterCreate, current_user: User,
) -> Lifter:
    """Kreiraj natjecatelja s ownership provjerom."""
    _check_club_access(current_user, club_id)
    lifter = Lifter(
        first_name=body.first_name,
        last_name=body.last_name,
        birth_date=body.birth_date,
        gender=body.gender,
        club_id=club_id,
    )
    return await lifter_repo.create(db, lifter)


async def update_lifter(
    db: AsyncSession, club_id: int, lifter_id: int,
    body: LifterUpdate, current_user: User,
) -> Lifter:
    """Ažuriraj natjecatelja (parcijalno) s ownership provjerom."""
    lifter = await get_lifter(db, club_id, lifter_id, current_user)
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(lifter, field, value)
    await db.flush()
    return lifter


async def delete_lifter(
    db: AsyncSession, club_id: int, lifter_id: int, current_user: User,
) -> None:
    """Obriši natjecatelja s ownership provjerom."""
    lifter = await get_lifter(db, club_id, lifter_id, current_user)
    await lifter_repo.delete(db, lifter)
