from typing import List

from sqlalchemy import String, Text
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Vacancy(Base):
    __tablename__ = "vacancy"

    id: Mapped[int] = mapped_column(primary_key=True)

    parsing_date: Mapped[str | None] = mapped_column(String(30))
    vacancy_id: Mapped[str | None] = mapped_column(String(20))

    role: Mapped[str | None] = mapped_column(String(120))
    title: Mapped[str | None] = mapped_column(String(120))
    salary: Mapped[str | None] = mapped_column(String(40))
    experience: Mapped[str | None] = mapped_column(String(30))
    employment_mode: Mapped[str | None] = mapped_column(String(30))
    accept_temporary: Mapped[str | None] = mapped_column(String(100))
    company_name: Mapped[str | None] = mapped_column(String(50))
    location: Mapped[str | None] = mapped_column(String(50))
    vacancy_description: Mapped[str | None] = mapped_column(Text())
    skills: Mapped[List[str] | None] = mapped_column(ARRAY(String))
    creation_time: Mapped[str | None] = mapped_column(String(40))
