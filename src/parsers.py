import time
from tqdm import tqdm

from src.utils import make_request
from src.models import Vacancy


class RoleParser:
    def __init__(self, config):
        self.config = config
        self.professional_roles = []

    def _parse_roles(self):
        json_data = make_request(
            self.config["professional_roles_url"], self.config["headers"]
        )
        if json_data is not None:
            for category in json_data["categories"]:
                for role in category["roles"]:
                    self.professional_roles.append(role)
        else:
            print("Can't get professional roles")

    def run(self):
        self._parse_roles()


class VacancyParser:
    def __init__(self, config, db):
        self.config = config
        self.db = db
        self.vacancies = []

    def _parse_page_count(self, professional_role):
        url = self.config["vacancies_search_url"].format(
            professional_role=professional_role["id"], page=0
        )

        json_data = make_request(url, headers=self.config["headers"])
        if json_data is not None:
            pages = int(json_data["pages"])
            return pages if pages < 39 else 39
        else:
            return None

    def _parse_vacancy_ids(self, db_vacancy_ids, professional_roles):
        vacancy_ids = []
        for professional_role in tqdm(professional_roles):
            pages = self._parse_page_count(professional_role)

            if pages is not None:
                pages = 1
                for page in range(pages):
                    url = self.config["vacancies_search_url"].format(
                        professional_role=professional_role["id"], page=page
                    )

                    json_data = make_request(
                        url, headers=self.config["headers"]
                    )
                    if json_data is not None:
                        for vacancy in json_data["items"][:1]:
                            if vacancy["id"] not in db_vacancy_ids:
                                vacancy_ids.append(vacancy["id"])
            else:
                print(f"Can't get page count for {professional_role['name']}")
        return vacancy_ids

    def _parse_vacancies(self, vacancy_ids):
        for vacancy_id in tqdm(vacancy_ids):
            url = self.config["vacancy_url"].format(vacancy_id=vacancy_id)
            json_data = make_request(url, headers=self.config["headers"])
            if json_data is not None:
                self.vacancies.append(json_data)
                time.sleep(0.3)
            else:
                print(f"Can't get {url}")
                time.sleep(2)

    def run(self):
        source_ids = self.db.select_source_ids(Vacancy)
        roles = self.db.select_roles()

        vacancy_ids = self._parse_vacancy_ids(source_ids, roles)
        vacancy_ids = list(set(vacancy_ids))
        self._parse_vacancies(vacancy_ids)
