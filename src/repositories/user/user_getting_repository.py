from dataclasses import dataclass
from typing import Optional

from patterns.repository import BaseRepository, IGettingRepository
from models import Usuario
from exceptions import UserNotFoundError


@dataclass
class UserGettingRepositoryParam:
    uuid_user: str


class UserGettingRepository(BaseRepository):
    def get(self, param: UserGettingRepositoryParam) -> Usuario:
        user: Optional[Usuario] = \
            self.session\
                    .query(Usuario)\
                    .filter(Usuario.id_uuid == param.uuid_user)\
                    .first()

        if not user:
            raise UserNotFoundError()

        return user

