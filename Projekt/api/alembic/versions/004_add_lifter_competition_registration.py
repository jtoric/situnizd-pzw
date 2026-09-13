"""add Lifter, Competition, Registration tables

Revision ID: 004
Revises: 003
Create Date: 2026-03-23

Tri nove tablice:
  - lifters: natjecatelji (FK → clubs)
  - competitions: natjecanja s rokovima
  - registrations: prijave (FK → lifters, competitions) s UniqueConstraint
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "004"
down_revision: Union[str, None] = "003"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "lifters",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("first_name", sa.String(80), nullable=False),
        sa.Column("last_name", sa.String(80), nullable=False),
        sa.Column("birth_date", sa.Date, nullable=False),
        sa.Column("gender", sa.String(1), nullable=False),
        sa.Column("club_id", sa.Integer, sa.ForeignKey("clubs.id"), nullable=False),
    )

    op.create_table(
        "competitions",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(200), nullable=False),
        sa.Column("date", sa.Date, nullable=False),
        sa.Column("location", sa.String(200), nullable=False),
        sa.Column("prelim_deadline", sa.DateTime(timezone=True), nullable=False),
        sa.Column("final_deadline", sa.DateTime(timezone=True), nullable=False),
    )

    op.create_table(
        "registrations",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("lifter_id", sa.Integer, sa.ForeignKey("lifters.id"), nullable=False),
        sa.Column("competition_id", sa.Integer, sa.ForeignKey("competitions.id"), nullable=False),
        sa.Column("category", sa.String(20), nullable=False),
        sa.Column("total", sa.Integer, nullable=False, server_default="0"),
        sa.Column("status", sa.String(20), server_default="active"),
        sa.Column("registered_at", sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.UniqueConstraint("lifter_id", "competition_id", name="uq_lifter_competition"),
    )


def downgrade() -> None:
    op.drop_table("registrations")
    op.drop_table("competitions")
    op.drop_table("lifters")
