from typing import Dict, List

from src.models import (
    Role,
    Vacancy,
    VacancyRoles,
    Skill,
    VacancySkills,
    Language,
    VacancyLanguages,
)


class RoleLoader:
    def __init__(self, config, db):
        self.config = config
        self.db = db

    def load(self, professional_roles):
        role_ids = self.db.select_source_ids(Role)

        professional_role_models = []
        for professional_role in professional_roles:
            if professional_role["id"] not in role_ids:
                professional_role_models.append(
                    Role.from_json(professional_role)
                )

        self.db.insert(professional_role_models)


class VacancyLoader:
    def __init__(self, config, db):
        self.config = config
        self.db = db

    def _get_vacancy_roles(self, vacancies) -> Dict:
        roles_dict = {}

        for vacancy in vacancies:
            role_ids = []
            roles = vacancy.get("professional_roles")
            for role in roles:
                role_ids.append(role["id"])
            roles_dict[vacancy["id"]] = role_ids

        return roles_dict

    def _get_vacancy_skills(self, vacancies) -> Dict:
        skills_dict = {}

        for vacancy in vacancies:
            skill_names = []
            skills = vacancy.get("key_skills")
            for skill in skills:
                skill_names.append(skill["name"])
            skills_dict[vacancy["id"]] = skill_names

        return skills_dict

    def _get_vacancy_languages(self, vacancies) -> Dict:
        languages_dict = {}

        for vacancy in vacancies:
            language_names = []
            languages = vacancy.get("languages")
            for language in languages:
                language_names.append(language["name"])
            languages_dict[vacancy["id"]] = language_names

        return languages_dict

    def _get_unique_skills(self, vacancies) -> List:
        skills = set()

        for vacancy in vacancies:
            vacancy_skills = vacancy.get("key_skills")
            if vacancy_skills is not None:
                for skill in vacancy_skills:
                    skills.add(skill["name"])
        return list(skills)

    def _get_unique_languages(self, vacancies) -> List:
        languages = set()

        for vacancy in vacancies:
            vacancy_languages = vacancy.get("languages")
            if vacancy_languages is not None:
                for language in vacancy_languages:
                    languages.add(language["name"])
        return list(languages)

    def load(self, vacancies):
        vacancy_ids = self.db.select_source_ids(Vacancy)

        processed_vacancies = []
        for vacancy in vacancies:
            if vacancy["id"] not in vacancy_ids:
                processed_vacancies.append(Vacancy.from_json(vacancy))

        self.db.insert(processed_vacancies)

        vacancy_source_id_map = self.db.select_source_ids_map(Vacancy)

        role_source_id_map = self.db.select_source_ids_map(Role)

        vacancy_roles = self._get_vacancy_roles(vacancies)
        vacancy_role_models = []
        for vacancy in vacancy_roles:
            vacancy_id = vacancy_source_id_map.get(vacancy)
            role_ids = vacancy_roles.get(vacancy)
            for role_id in role_ids:
                role_id = role_source_id_map.get(role_id)
                vacancy_role_models.append(
                    VacancyRoles(vacancy_id=vacancy_id, role_id=role_id)
                )

        self.db.insert(vacancy_role_models)

        skills = self._get_unique_skills(vacancies)

        skill_names = self.db.select_names(Skill)

        skill_models = []
        for skill in skills:
            if skill not in skill_names:
                skill_models.append(Skill(name=skill))

        self.db.insert(skill_models)

        vacancy_skill_map = self.db.select_names_map(Skill)

        vacancy_skills = self._get_vacancy_skills(vacancies)
        vacancy_skill_models = []
        for vacancy in vacancy_skills:
            vacancy_id = vacancy_source_id_map.get(vacancy)
            skill_names = vacancy_skills.get(vacancy)
            for skill_name in skill_names:
                skill_id = vacancy_skill_map.get(skill_name)
                vacancy_skill_models.append(
                    VacancySkills(vacancy_id=vacancy_id, skill_id=skill_id)
                )

        self.db.insert(vacancy_skill_models)

        languages = self._get_unique_languages(vacancies)

        language_names = self.db.select_names(Language)

        language_models = []
        for language in languages:
            if language not in language_names:
                language_models.append(Language(name=language))

        self.db.insert(language_models)

        vacancy_language_map = self.db.select_names_map(Language)

        vacancy_languages = self._get_vacancy_languages(vacancies)
        vacancy_language_models = []
        for vacancy in vacancy_languages:
            vacancy_id = vacancy_source_id_map.get(vacancy)
            language_names = vacancy_languages.get(vacancy)
            for language_name in language_names:
                language_id = vacancy_language_map.get(language_name)
                vacancy_language_models.append(
                    VacancyLanguages(
                        vacancy_id=vacancy_id, language_id=language_id
                    )
                )

        self.db.insert(vacancy_language_models)
