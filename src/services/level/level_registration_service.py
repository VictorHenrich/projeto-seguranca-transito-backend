from patterns import InterfaceService, CrudRepository
from repositories.level import CrudLevelRepository
from .entities import LevelRegistration
from models import Nivel





class LevelRegistrationService(InterfaceService[LevelRegistration]):
    def execute(self, param: LevelRegistration):
        repository: CrudRepository[Nivel] = CrudLevelRepository()

        repository.create(param.departament, param)