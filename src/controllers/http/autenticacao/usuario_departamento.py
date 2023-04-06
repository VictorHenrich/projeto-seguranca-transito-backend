from dataclasses import dataclass

from server import App
from middlewares.http import BodyRequestValidationMiddleware
from exceptions import DepartamentNotFoundError, UserNotFoundError
from services.agent import AgentAuthorizationService, AgentAuthorizationServiceProps
from patterns.service import IService
from server.http import (
    Controller,
    ResponseDefaultJSON,
    ResponseInauthorized,
    ResponseSuccess,
)


@dataclass
class DepartamentUserAuthRequestBody:
    departamento: str
    usuario: str
    senha: str


@App.http.add_controller("/autenticacao/departamento")
class AutenticaoUsuarioDepartamentoController(Controller):
    @BodyRequestValidationMiddleware.apply(DepartamentUserAuthRequestBody)
    def post(self, body_request: DepartamentUserAuthRequestBody) -> ResponseDefaultJSON:
        try:
            service: IService[
                AgentAuthorizationServiceProps, str
            ] = AgentAuthorizationService()

            service_props: AgentAuthorizationServiceProps = (
                AgentAuthorizationServiceProps(
                    departament_access=body_request.departamento,
                    user=body_request.usuario,
                    password=body_request.senha,
                )
            )

            token: str = service.execute(service_props)

            return ResponseSuccess(data=token)

        except UserNotFoundError as error:
            return ResponseInauthorized(data=str(error))

        except DepartamentNotFoundError as error:
            return ResponseInauthorized(data=str(error))
