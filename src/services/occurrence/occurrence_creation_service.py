from start import app
from patterns.repository import ICreationRepository
from patterns.service import IService
from models import Usuario, Departamento
from services.departament import DepartamentGettingUUIDService
from repositories.occurrence import (
    OccurrenceCreationRepository,
    OccurrenceCreationRepositoryParam
)


class OccurrenceCreationService:
    def execute(
        self,
        user: Usuario,
        uuid_departament: str,
        description: str,
        obs: str
    ) -> None:
        
        with app.databases.create_session() as session:
            departament_getting_service: IService[Departamento] = DepartamentGettingUUIDService()

            departament: Departamento = \
                departament_getting_service.execute(
                    uuid_departament=uuid_departament
                )

            occurrence_creation_repo_param: OccurrenceCreationRepositoryParam = \
                OccurrenceCreationRepositoryParam(
                    user=user,
                    departament=departament,
                    description=description,
                    obs=obs
                )

            occurrence_creation_repository: ICreationRepository[OccurrenceCreationRepositoryParam] = \
                OccurrenceCreationRepository(session)

            occurrence_creation_repository.create(occurrence_creation_repo_param)

            session.commit()

        

        