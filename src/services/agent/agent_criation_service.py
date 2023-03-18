from dataclasses import dataclass

from start import app
from patterns.repository import ICreateRepository
from models import Departament
from repositories.agent import (
    AgentCreateRepository,
    AgentCreateRepositoryParam,
)


@dataclass
class AgentCriationServiceProps:
    departament: Departament
    name: str
    access: str
    password: str
    position: str


class AgentCriationService:
    def execute(self, props: AgentCriationServiceProps) -> None:
        with app.databases.create_session() as session:
            creating_repository: ICreateRepository[
                AgentCreateRepositoryParam, None
            ] = AgentCreateRepository(session)

            creating_repository.create(props)

            session.commit()
