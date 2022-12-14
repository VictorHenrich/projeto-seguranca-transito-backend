from flask import request
from typing import Optional
from datetime import datetime

from server.http import Middleware, ResponseInauthorized
from server.utils import UtilsJWT, UtilsExcept
from patterns.service import IService
from models import Usuario
from services.user import UserGettingService
from exceptions import (
    AuthorizationNotFoundHeader, 
    TokenTypeNotBearerError,
    ExpiredTokenError,
    UserNotFoundError
)
from utils.entities import PayloadUserJWT
from start import app



class UserAuthenticationMiddleware(Middleware):
    @classmethod
    def handle(cls):
        token: Optional[str] = request.headers.get('Authorization')

        if not token:
            raise AuthorizationNotFoundHeader()

        if 'Bearer' not in token:
            raise TokenTypeNotBearerError()

        token = token.replace('Bearer ', '')

        payload: PayloadUserJWT = \
            UtilsJWT.decode(token, app.http.configs.secret_key, PayloadUserJWT)

        if payload.expired <= datetime.now().timestamp():
            raise ExpiredTokenError()

        service: IService[Usuario] = UserGettingService()

        user: Usuario = service.execute(uuid_user=payload.uuid_user)

        return {"auth": user}

    @classmethod
    def catch(cls, exception: Exception):
        validation: bool = UtilsExcept.fired(
            exception,
            ExpiredTokenError,
            UserNotFoundError,
            TokenTypeNotBearerError,
            AuthorizationNotFoundHeader
        )

        if validation:
            return ResponseInauthorized(data=str(exception))

        raise exception
        