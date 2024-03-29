from dataclasses import dataclass
from datetime import datetime

from server import Databases, HttpServer
from utils.jwt import JWTUtils
from utils import JWTUtils
from utils.entities import PayloadUserJWT
from patterns.repository import IFindRepository
from models import User
from repositories.user import UserFindRepository, UserFindRepositoryParams
from exceptions import (
    TokenTypeNotBearerError,
    ExpiredTokenError,
)


@dataclass
class FindUserProps:
    user_uuid: str


class AuthVerificationService:
    def __init__(self, token: str) -> None:
        self.__token: str = token

    def execute(self) -> User:
        if not self.__token or "Bearer" not in self.__token:
            raise TokenTypeNotBearerError()

        token = self.__token.replace("Bearer ", "")

        payload: PayloadUserJWT = JWTUtils.decode(
            token, HttpServer.config.secret_key, class_=PayloadUserJWT
        )

        if payload.expired <= datetime.now().timestamp():
            raise ExpiredTokenError()

        with Databases.create_session() as session:
            user_find: IFindRepository[
                UserFindRepositoryParams, User
            ] = UserFindRepository(session)

            user: User = user_find.find_one(FindUserProps(payload.user_uuid))

            return user
