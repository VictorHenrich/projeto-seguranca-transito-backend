from flask_socketio import SocketIO
from typing import Optional, Protocol, Mapping, Any, Type, Union
from ..http.server import HttpServer
from .controller import Controller


class ConfigSocket(Protocol):
    host: Optional[str] = None
    port: Optional[Union[str, int]] = None
    debug: bool = False


class SocketServer(SocketIO):
    def __init__(
        self, app: HttpServer, config: ConfigSocket, **options: Mapping[str, Any]
    ):
        self.__app: HttpServer = app

        self.__config: ConfigSocket = config

        super().__init__(app.application, **options)

    @property
    def config(self) -> ConfigSocket:
        return self.__config

    def start_app(self) -> None:
        self.run(self.__app.application, self.__config.host, self.__config.port)

    def add_route(self, controller: Type[Controller]) -> None:
        self.on_namespace(controller())
