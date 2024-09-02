from typing import Type, List, Dict

from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models import Base, Role


class Database:
    def __init__(self, engine):
        self.engine = engine

    def create_all(self) -> None:
        Base.metadata.create_all(bind=self.engine)

    def drop_all(self) -> None:
        Base.metadata.drop_all(bind=self.engine)

    def _select(self, statement):
        with Session(self.engine) as session:
            result = session.execute(statement)
        return result

    def insert(self, rows):
        with Session(self.engine) as session:
            session.add_all(rows)
            session.commit()

    def select_source_ids(self, model: Type[Base]) -> List:
        statement = select(model.source_id)
        return [row[0] for row in self._select(statement)]

    def select_source_ids_map(self, model: Type[Base]) -> Dict:
        statement = select(model.id, model.source_id)
        return {row[1]: row[0] for row in self._select(statement)}

    def select_names(self, model: Type[Base]) -> List:
        statement = select(model.name)
        return [row[0] for row in self._select(statement)]

    def select_names_map(self, model: Type[Base]) -> Dict:
        statement = select(model.id, model.name)
        return {row[1]: row[0] for row in self._select(statement)}

    def select_roles(self):
        with Session(self.engine) as session:
            roles = [
                {"id": row[0], "name": row[1]}
                for row in session.execute(select(Role.source_id, Role.name))
            ]
        return roles
