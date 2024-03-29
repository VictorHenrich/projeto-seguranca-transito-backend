from server import SocketServer
from server.websocket import SocketController, ConnectionController
from models import User
from server.websocket import SocketMiddleware
from middlewares.websocket import UserAuthenticationMiddleware


class ConnectionUser(ConnectionController):
    def __init__(self, id: str, auth: User) -> None:
        self.__auth: User = auth
        super().__init__(id)

    @property
    def auth(self) -> User:
        return self.__auth


autentication_middleware: SocketMiddleware[None] = UserAuthenticationMiddleware()


@SocketServer.add_controller("/usuario")
class UserController(SocketController[ConnectionUser]):
    autentication_middleware.apply()

    def on_open(self, connection: ConnectionController, auth: User) -> ConnectionUser:
        print("UM USUÁRIO SE CONECTOUUUU!")

        return ConnectionUser(connection.id, auth)

    def on_send_message(self) -> None:
        pass
