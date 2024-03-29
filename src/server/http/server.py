from typing import (
    Any,
    Union,
    Type,
    Callable,
)
from flask import Flask, Request, request
from flask_cors import CORS
from flask_restful import Api
from dataclasses import dataclass

from .controller import HttpController


@dataclass
class HttpServerConfig:
    host: str
    port: Union[str, int]
    secret_key: str
    debug: bool


class HttpServer:
    __app: Flask = Flask(__name__)

    __api: Api = Api(__app)

    __cors: CORS = CORS(__app)

    __global_request: Request = request

    __config: HttpServerConfig = HttpServerConfig(
        host="localhost", port=3000, secret_key="", debug=True
    )

    @classmethod
    @property
    def config(cls) -> HttpServerConfig:
        return cls.__config

    @classmethod
    @property
    def cors(cls) -> CORS:
        return cls.__cors

    @classmethod
    @property
    def global_request(cls) -> Request:
        return cls.__global_request

    @classmethod
    def run(cls) -> None:
        cls.__app.run(
            host=cls.__config.host,
            port=int(cls.__config.port),
            debug=cls.__config.debug,
        )

    @classmethod
    def add_controller(
        cls, *urls: str, **kwargs: Any
    ) -> Callable[[Type[HttpController]], Type[HttpController]]:
        def wrapper(c: Type[HttpController]) -> Type[HttpController]:
            cls.__api.add_resource(c, *urls, **kwargs)

            return c

        return wrapper

    @classmethod
    def set_config(cls, config: HttpServerConfig) -> None:
        cls.__config = config

    @classmethod
    def set_global_request(cls, global_request: Request) -> None:
        cls.__global_request = global_request
