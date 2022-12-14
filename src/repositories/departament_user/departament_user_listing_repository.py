from typing import List
from dataclasses import dataclass

from patterns.repository import BaseRepository
from models import Departamento, UsuarioDepartamento


@dataclass
class DepartamentUserListingRepositoryParam:
    departament: Departamento


class DepartamentUserListingRepository(BaseRepository):
    def list(self, param: DepartamentUserListingRepositoryParam) -> List[UsuarioDepartamento]:
        departament_users: List[UsuarioDepartamento] = \
            self.session\
                    .query(UsuarioDepartamento)\
                    .join(Departamento, UsuarioDepartamento.id_departamento == Departamento.id)\
                    .filter(UsuarioDepartamento.id_departamento == param.departament.id)\
                    .all()

        return departament_users
