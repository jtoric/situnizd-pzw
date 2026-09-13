# =============================================================
# competition_service.py — Poslovna logika za natjecanja
# =============================================================
# Admin kreira i ažurira natjecanja.
# Svi autenticirani korisnici mogu čitati (list, get).
# =============================================================

from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import AppError
from app.models.competition import Competition
from app.repositories import competition_repo
from app.schemas.competition import CompetitionCreate, CompetitionUpdate


async def list_competitions(db: AsyncSession) -> list[Competition]:
    """Dohvati sva natjecanja."""
    return await competition_repo.get_all(db)


async def get_competition(db: AsyncSession, comp_id: int) -> Competition:
    """Dohvati natjecanje po ID-u ili baci 404."""
    comp = await competition_repo.get_by_id(db, comp_id)
    if not comp:
        raise AppError("not_found", "Natjecanje nije pronađeno", 404)
    return comp


async def create_competition(
    db: AsyncSession, body: CompetitionCreate,
) -> Competition:
    """Admin kreira novo natjecanje."""
    comp = Competition(
        name=body.name,
        date=body.date,
        location=body.location,
        prelim_deadline=body.prelim_deadline,
        final_deadline=body.final_deadline,
    )
    return await competition_repo.create(db, comp)


async def update_competition(
    db: AsyncSession, comp_id: int, body: CompetitionUpdate,
) -> Competition:
    """Admin ažurira natjecanje (parcijalno)."""
    comp = await get_competition(db, comp_id)
    for field, value in body.model_dump(exclude_unset=True).items():
        setattr(comp, field, value)
    await db.flush()
    return comp
