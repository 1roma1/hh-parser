from datetime import date
from typing import Type, TypeVar, List

from sqlalchemy import String, Text, ForeignKey
from sqlalchemy.ext.declarative import AbstractConcreteBase
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


VacancyType = TypeVar("VacancyType")
RoleType = TypeVar("RoleType")


class Base(DeclarativeBase):
    pass


class SourceIdModel(AbstractConcreteBase, Base):
    strict_attrs = True

    id: Mapped[int] = mapped_column(primary_key=True)
    source_id: Mapped[str | None] = mapped_column(String(20))


class NamedModel(AbstractConcreteBase, Base):
    strict_attrs = True

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str | None] = mapped_column(String(200))


class VacancyAssociationTable(AbstractConcreteBase, Base):
    strict_attrs = True

    vacancy_id: Mapped[int] = mapped_column(
        ForeignKey("vacancy.id"), primary_key=True
    )


class Vacancy(SourceIdModel):
    __tablename__ = "vacancy"

    parsing_date: Mapped[str | None] = mapped_column(String(30))

    title: Mapped[str | None] = mapped_column(String(120))
    description: Mapped[str | None] = mapped_column(Text())
    company: Mapped[str | None] = mapped_column(String(160))
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
    def from_json(cls: Type[VacancyType], json: dict) -> VacancyType:
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


class Role(SourceIdModel):
    __tablename__ = "role"

    name: Mapped[str | None] = mapped_column(String(120))

    vacancies: Mapped[List["VacancyRoles"]] = relationship(
        back_populates="role"
    )

    @classmethod
    def from_json(cls: Type[RoleType], json: dict) -> RoleType:
        kwargs = {
            "source_id": json["id"],
            "name": json["name"],
        }
        return cls(**kwargs)


class Skill(NamedModel):
    __tablename__ = "skill"

    vacancies: Mapped[List["VacancySkills"]] = relationship(
        back_populates="skill"
    )


class Language(NamedModel):
    __tablename__ = "language"

    vacancies: Mapped[List["VacancyLanguages"]] = relationship(
        back_populates="language"
    )


class VacancyRoles(VacancyAssociationTable):
    __tablename__ = "vacancy_roles"

    role_id: Mapped[int] = mapped_column(
        ForeignKey("role.id"), primary_key=True
    )

    vacancy: Mapped["Vacancy"] = relationship(back_populates="roles")
    role: Mapped["Role"] = relationship(back_populates="vacancies")


class VacancySkills(VacancyAssociationTable):
    __tablename__ = "vacancy_skills"

    skill_id: Mapped[int] = mapped_column(
        ForeignKey("skill.id"), primary_key=True
    )

    vacancy: Mapped["Vacancy"] = relationship(back_populates="skills")
    skill: Mapped["Skill"] = relationship(back_populates="vacancies")


class VacancyLanguages(VacancyAssociationTable):
    __tablename__ = "vacancy_languages"

    language_id: Mapped[int] = mapped_column(
        ForeignKey("language.id"), primary_key=True
    )

    vacancy: Mapped["Vacancy"] = relationship(back_populates="languages")
    language: Mapped["Language"] = relationship(back_populates="vacancies")
