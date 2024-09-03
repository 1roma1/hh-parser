from typing import Dict, List, Type, TypeVar

from src.models import (
    Role,
    Vacancy,
    VacancyRoles,
    Skill,
    VacancySkills,
    Language,
    VacancyLanguages,
    VacancyAssociationTable,
)

from src.db import Database, NamedModelType

VacancyAssociationType = TypeVar(
    "VacancyAssociationType", bound=VacancyAssociationTable
)


class RoleLoader:
    def __init__(self, db: Database) -> None:
        self.db = db

    def load(self, professional_roles: List[Dict]) -> None:
        role_ids = self.db.select_source_ids(Role)

        professional_role_models = []
        for professional_role in professional_roles:
            if professional_role["id"] not in role_ids:
                professional_role_models.append(
                    Role.from_json(professional_role)
                )

        self.db.insert(professional_role_models)


class VacancyLoader:
    def __init__(self, db: Database) -> None:
        self.db = db

    def _get_unique_items(
        self, vacancies: List[Dict], items_key: str, item_key: str
    ) -> List:
        items = set()

        for vacancy in vacancies:
            vacancy_items = vacancy.get(items_key)
            if vacancy_items is not None:
                for item in vacancy_items:
                    items.add(item[item_key])
        return list(items)

    def _get_vacancy_items(
        self, vacancies: List[Dict], items_key: str, item_key: str
    ) -> Dict:
        items_dict = {}

        for vacancy in vacancies:
            items = []
            vacancy_items = vacancy.get(items_key)
            if vacancy_items is not None:
                for vacancy_item in vacancy_items:
                    items.append(vacancy_item[item_key])
            items_dict[vacancy["id"]] = items

        return items_dict

    def _load_new_vacancy_items(
        self,
        vacancies: List[Dict],
        vacancy_map: Dict,
        items_map: Dict,
        items_key: str,
        item_key: str,
        model: Type[VacancyAssociationType],
        model_field: str,
    ) -> None:
        items_by_vacancy = self._get_vacancy_items(
            vacancies, items_key, item_key
        )
        vacancy_item_models = []
        for vacancy in items_by_vacancy:
            vacancy_id = vacancy_map.get(vacancy)
            items = items_by_vacancy.get(vacancy)
            if items is not None:
                for item in items:
                    item_id = items_map.get(item)
                    row = {"vacancy_id": vacancy_id, model_field: item_id}
                    vacancy_item_models.append(model(**row))

        self.db.insert(vacancy_item_models)

    def _load_new_items(
        self, items: List, model: Type[NamedModelType]
    ) -> None:
        item_names = self.db.select_names(model)

        item_models = []
        for item in items:
            if item not in item_names:
                item_models.append(model(name=item))

        self.db.insert(item_models)

    def load(self, vacancies: List[Dict]) -> None:
        vacancy_ids = self.db.select_source_ids(Vacancy)

        processed_vacancies = []
        for vacancy in vacancies:
            if vacancy["id"] not in vacancy_ids:
                processed_vacancies.append(Vacancy.from_json(vacancy))

        self.db.insert(processed_vacancies)

        for items_key, item_key, named_model in [
            ("key_skills", "name", Skill),
            ("languages", "name", Language),
        ]:
            items = self._get_unique_items(vacancies, items_key, item_key)
            self._load_new_items(items, named_model)

        vacancy_map = self.db.select_source_ids_map(Vacancy)
        role_map = self.db.select_source_ids_map(Role)
        skill_map = self.db.select_names_map(Skill)
        lang_map = self.db.select_names_map(Language)

        for item_map, items_key, item_key, model, model_field in [
            (role_map, "professional_roles", "id", VacancyRoles, "role_id"),
            (skill_map, "key_skills", "name", VacancySkills, "skill_id"),
            (lang_map, "languages", "name", VacancyLanguages, "language_id"),
        ]:
            self._load_new_vacancy_items(
                vacancies,
                vacancy_map,
                item_map,
                items_key,
                item_key,
                model,
                model_field,
            )
