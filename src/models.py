# from typing import List
# from sqlalchemy.dialects.postgresql import ARRAY
from datetime import date
from typing import Type, TypeVar, List

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


T = TypeVar("T")


class Base(DeclarativeBase):
    pass


class Vacancy(Base):
    __tablename__ = "vacancy"

    id: Mapped[int] = mapped_column(primary_key=True)

    parsing_date: Mapped[str | None] = mapped_column(String(30))
    source_id: Mapped[str | None] = mapped_column(String(20))

    title: Mapped[str | None] = mapped_column(String(120))
    description: Mapped[str | None] = mapped_column(Text())
    company: Mapped[str | None] = mapped_column(String(50))
    employment: Mapped[str | None] = mapped_column(String(30))
    experience: Mapped[str | None] = mapped_column(String(30))
    salary: Mapped[str | None] = mapped_column(String(40))
    published_at: Mapped[str | None] = mapped_column(String(40))

    roles: Mapped[List["VacancyRoles"]] = relationship(
        back_populates="vacancy"
    )

    skills: Mapped[List["VacancySkills"]] = relationship(
        back_populates="vacancy"
    )

    languages: Mapped[List["VacancyLanguages"]] = relationship(
        back_populates="vacancy"
    )

    @classmethod
    def from_json(cls: Type[T], json: dict) -> T:
        kwargs = {}
        kwargs["source_id"] = json["id"]
        kwargs["parsing_date"] = date.today().strftime("%Y-%m-%d")
        kwargs["published_at"] = json["published_at"]
        kwargs["title"] = json["name"]
        kwargs["description"] = json["description"]
        kwargs["company"] = json["employer"]["name"]
        kwargs["employment"] = json["employment"]["name"]
        kwargs["experience"] = json["experience"]["name"]

        if json["salary"] is not None:
            salary = ""
            from_ = json["salary"]["from"]
            to = json["salary"]["to"]
            currency = json["salary"]["currency"]
            if from_ is not None:
                salary += str(from_)
                if to is not None:
                    salary += "-" + str(to)
            elif to is not None:
                salary += str(to)
            salary += " " + currency

            kwargs["salary"] = salary
        else:
            kwargs["salary"] = None

        return cls(**kwargs)


class Role(Base):
    __tablename__ = "role"

    id: Mapped[int] = mapped_column(primary_key=True)

    source_id: Mapped[str | None] = mapped_column(String(20))
    name: Mapped[str | None] = mapped_column(String(120))

    vacancies: Mapped[List["VacancyRoles"]] = relationship(
        back_populates="role"
    )

    @classmethod
    def from_json(cls: Type[T], json: dict) -> T:
        kwargs = {
            "source_id": json["id"],
            "name": json["name"],
        }
        return cls(**kwargs)


class Skill(Base):
    __tablename__ = "skill"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str | None] = mapped_column(String(200))

    vacancies: Mapped[List["VacancySkills"]] = relationship(
        back_populates="skill"
    )


class Language(Base):
    __tablename__ = "language"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str | None] = mapped_column(String(20))

    vacancies: Mapped[List["VacancyLanguages"]] = relationship(
        back_populates="language"
    )


class VacancyRoles(Base):
    __tablename__ = "vacancy_roles"

    vacancy_id: Mapped[int] = mapped_column(
        ForeignKey("vacancy.id"), primary_key=True
    )
    role_id: Mapped[int] = mapped_column(
        ForeignKey("role.id"), primary_key=True
    )

    vacancy: Mapped["Vacancy"] = relationship(back_populates="roles")
    role: Mapped["Role"] = relationship(back_populates="vacancies")


class VacancySkills(Base):
    __tablename__ = "vacancy_skills"

    vacancy_id: Mapped[int] = mapped_column(
        ForeignKey("vacancy.id"), primary_key=True
    )
    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skill.id"), primary_key=True
    )

    vacancy: Mapped["Vacancy"] = relationship(back_populates="skills")
    skill: Mapped["Skill"] = relationship(back_populates="vacancies")


class VacancyLanguages(Base):
    __tablename__ = "vacancy_languages"

    vacancy_id: Mapped[int] = mapped_column(
        ForeignKey("vacancy.id"), primary_key=True
    )
    language_id: Mapped[int] = mapped_column(
        ForeignKey("language.id"), primary_key=True
    )

    vacancy: Mapped["Vacancy"] = relationship(back_populates="languages")
    language: Mapped["Language"] = relationship(back_populates="vacancies")
