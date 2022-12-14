from dataclasses import dataclass

from patterns.repository import BaseRepository, IAuthRepository
from models import Usuario
from exceptions import UserNotFoundError


@dataclass
class UserAuthRepositoryParam:
    email: str
    password: str


class UserAuthRepository(BaseRepository):
    def auth(self, param: UserAuthRepositoryParam) -> Usuario:
        user: Usuario = \
            self.session\
                    .query(Usuario)\
                    .filter(
                        Usuario.email == param.email.upper(),
                        Usuario.senha == param.password
                    )\
                    .first()

        if not user:
            raise UserNotFoundError()

        return user