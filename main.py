from src.parsers import RoleParser, VacancyParser
from src.loaders import RoleLoader, VacancyLoader
from src.utils import load_configuration, get_db_connection_engine, json_dump
from src.db import Database


def main() -> None:
    config = load_configuration("config.yaml")
    engine = get_db_connection_engine()

    db = Database(engine)

    role_parser = RoleParser(config)
    role_loader = RoleLoader(db)

    role_parser.run()
    role_loader.load(role_parser.professional_roles)

    vacancy_parser = VacancyParser(config, db)
    vacancy_loader = VacancyLoader(db)

    vacancy_parser.run()
    json_dump("data/data.json", vacancy_parser.vacancies)
    vacancy_loader.load(vacancy_parser.vacancies)


if __name__ == "__main__":
    main()
