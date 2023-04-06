from dataclasses import dataclass

from server import App
from patterns.repository import IUpdateRepository
from repositories.occurrence import (
    OccurrenceUpdateRepository,
    OccurrenceUpdateRepositoryParam,
)


@dataclass
class OccurrenceUpdateServiceProps:
    uuid_occurrence: str
    description: str
    obs: str


class OccurrenceUpdateService:
    def execute(self, props: OccurrenceUpdateServiceProps) -> None:
        with App.databases.create_session() as session:
            update_repository: IUpdateRepository[
                OccurrenceUpdateRepositoryParam, None
            ] = OccurrenceUpdateRepository(session)

            update_repository.update(props)

            session.commit()
