import os
import re
import requests
from datetime import date
from typing import Dict

from tqdm import tqdm
from bs4 import BeautifulSoup

from src.utils import json_dump, json_load


class Parser:
    def __init__(
        self,
        url_template: str,
        headers: Dict,
        datadir: str,
    ):
        self.url_template = url_template
        self.headers = headers

        self.datadir = datadir

    def __get_page_count(self, role_id):
        url = self.url_template.format(role=role_id, page=0)
        resp = requests.get(url, headers=self.headers)

        bs = BeautifulSoup(resp.text, "html.parser")
        pages = bs.find_all("a", {"data-qa": "pager-page"})

        if len(pages) > 0:
            page_count = max([int(page.text) for page in pages])
        else:
            page_count = 1

        return page_count

    def __parse_vacancy_links(self, roles):
        total_links = {}
        for role_id in roles:
            role_links = []
            print(roles[role_id])
            page_count = self.__get_page_count(role_id)
            for page in tqdm(range(page_count)):
                url = self.url_template.format(role=role_id, page=page)
                resp = requests.get(url, headers=self.headers)

                if resp.ok:
                    links = re.findall(
                        r"https://rabota.by/vacancy/\d*", resp.text
                    )
                    links = list(set(links))
                    role_links += links
            total_links[roles[role_id]] = role_links
            break
        return total_links

    def __parse_vacancy(self, url, role):
        resp = requests.get(url, headers=self.headers)
        bs = BeautifulSoup(resp.text, "html.parser")

        vacancy = {}
        vacancy["role"] = role
        vacancy["vacancy_id"] = url.split("/")[-1]

        vacancy_title = bs.find("h1", {"data-qa": "vacancy-title"})
        vacancy["title"] = (
            vacancy_title.text if vacancy_title is not None else None
        )

        vacancy_salary = bs.find("div", {"data-qa": "vacancy-salary"})
        vacancy["salary"] = (
            vacancy_salary.text.replace("\xa0", "")
            if vacancy_salary is not None
            else None
        )

        vacancy_experience = bs.find("span", {"data-qa": "vacancy-experience"})
        vacancy["experience"] = (
            vacancy_experience.text if vacancy_experience is not None else None
        )

        vacancy_employment_mode = bs.find(
            "p", {"data-qa": "vacancy-view-employment-mode"}
        )
        vacancy["employment_mode"] = (
            vacancy_employment_mode.text
            if vacancy_employment_mode is not None
            else None
        )

        vacancy_accept_temporary = bs.find(
            "p", {"data-qa": "vacancy-view-accept-temporary"}
        )
        vacancy["accept_temporary"] = (
            vacancy_accept_temporary.text
            if vacancy_accept_temporary is not None
            else None
        )

        vacancy_company_name = bs.find(
            "a", {"data-qa": "vacancy-company-name"}
        )
        vacancy["company_name"] = (
            vacancy_company_name.text.replace("\xa0", " ")
            if vacancy_company_name is not None
            else None
        )

        vacancy_location = bs.find("p", {"data-qa": "vacancy-view-location"})
        vacancy["location"] = (
            vacancy_location.text if vacancy_location is not None else None
        )

        vacancy_description = bs.find(
            "div", {"data-qa": "vacancy-description"}
        )
        vacancy["description"] = (
            vacancy_description.text
            if vacancy_description is not None
            else None
        )

        skill_elements = bs.find_all("li", {"data-qa": "skills-element"})
        skills = []
        for skill_element in skill_elements:
            skills.append(skill_element.text)
        vacancy["skills"] = skills

        creation_time = bs.find(
            "p", {"class": "vacancy-creation-time-redesigned"}
        )
        vacancy["creation_time"] = (
            creation_time.text.replace("\xa0", " ")
            if creation_time is not None
            else None
        )

        return vacancy

    def __parse_vacancies(self, vacancy_links):
        vacancies = []
        for role in vacancy_links:
            print(role)
            role_links = vacancy_links[role]
            for link in tqdm(role_links):
                vacancy = self.__parse_vacancy(link, role)
                vacancies.append(vacancy)
        return vacancies

    def run(self):
        """Main parsing function"""

        roles = json_load("roles.json")
        vacancy_links = self.__parse_vacancy_links(roles)
        self.vacancies = self.__parse_vacancies(vacancy_links)

    def save_to_file(self):
        """Saving parsed data to json file"""

        filename = f"vacancies_{date.today().strftime('%d_%m_%y')}.json"
        json_dump(os.path.join(self.datadir, filename), self.vacancies)
