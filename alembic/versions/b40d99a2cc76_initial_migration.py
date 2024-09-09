"""initial migration

Revision ID: b40d99a2cc76
Revises:
Create Date: 2024-09-09 16:13:37.147185

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


revision: str = "b40d99a2cc76"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "language",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "role",
        sa.Column("source_id", sa.String(length=20), nullable=True),
        sa.Column("name", sa.String(length=120), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "skill",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=200), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "vacancy",
        sa.Column("parsing_date", sa.String(length=30), nullable=True),
        sa.Column("title", sa.String(length=120), nullable=True),
        sa.Column("description", sa.Text(), nullable=True),
        sa.Column("company", sa.String(length=160), nullable=True),
        sa.Column("employment", sa.String(length=30), nullable=True),
        sa.Column("experience", sa.String(length=30), nullable=True),
        sa.Column("salary", sa.String(length=40), nullable=True),
        sa.Column("published_at", sa.String(length=40), nullable=True),
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("source_id", sa.String(length=20), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "vacancy_languages",
        sa.Column("language_id", sa.Integer(), nullable=False),
        sa.Column("vacancy_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["language_id"],
            ["language.id"],
        ),
        sa.ForeignKeyConstraint(
            ["vacancy_id"],
            ["vacancy.id"],
        ),
        sa.PrimaryKeyConstraint("language_id", "vacancy_id"),
    )
    op.create_table(
        "vacancy_roles",
        sa.Column("role_id", sa.Integer(), nullable=False),
        sa.Column("vacancy_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["role.id"],
        ),
        sa.ForeignKeyConstraint(
            ["vacancy_id"],
            ["vacancy.id"],
        ),
        sa.PrimaryKeyConstraint("role_id", "vacancy_id"),
    )
    op.create_table(
        "vacancy_skills",
        sa.Column("skill_id", sa.Integer(), nullable=False),
        sa.Column("vacancy_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["skill_id"],
            ["skill.id"],
        ),
        sa.ForeignKeyConstraint(
            ["vacancy_id"],
            ["vacancy.id"],
        ),
        sa.PrimaryKeyConstraint("skill_id", "vacancy_id"),
    )


def downgrade() -> None:
    op.drop_table("vacancy_skills")
    op.drop_table("vacancy_roles")
    op.drop_table("vacancy_languages")
    op.drop_table("vacancy")
    op.drop_table("skill")
    op.drop_table("role")
    op.drop_table("language")
