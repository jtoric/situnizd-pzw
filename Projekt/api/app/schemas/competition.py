# =============================================================
# competition.py — Pydantic scheme za Competition entitet
# =============================================================

import datetime

from pydantic import BaseModel, Field, field_validator


class CompetitionCreate(BaseModel):
    """POST /competitions — admin kreira natjecanje."""
    name: str = Field(min_length=1, max_length=200)
    date: datetime.date
    location: str = Field(min_length=1, max_length=200)
    prelim_deadline: datetime.datetime
    final_deadline: datetime.datetime

    @field_validator("final_deadline")
    @classmethod
    def final_after_prelim(cls, v: datetime.datetime, info) -> datetime.datetime:
        prelim = info.data.get("prelim_deadline")
        if prelim and v <= prelim:
            raise ValueError("final_deadline mora biti nakon prelim_deadline")
        return v


class CompetitionUpdate(BaseModel):
    """PATCH /competitions/{id} — admin ažurira natjecanje."""
    name: str | None = Field(default=None, min_length=1, max_length=200)
    date: datetime.date | None = None
    location: str | None = Field(default=None, min_length=1, max_length=200)
    prelim_deadline: datetime.datetime | None = None
    final_deadline: datetime.datetime | None = None


class CompetitionResponse(BaseModel):
    """Odgovor s podacima o natjecanju."""
    id: int
    name: str
    date: datetime.date
    location: str
    prelim_deadline: datetime.datetime
    final_deadline: datetime.datetime

    model_config = {"from_attributes": True}
