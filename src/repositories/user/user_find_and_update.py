from typing import Protocol
from datetime import date

from patterns.repository import IFindRepository, BaseRepository
from models import User
from .user_find import UserFindRepository, UserFindRepositoryParams
from utils import CharUtils


class UserFindAndUpdateRepositoryParams(Protocol):
    user_uuid: str
    name: str
    email: str
    document: str
    document_rg: str
    telephone: str
    state_issuer: str
    address_state: str
    address_city: str
    address_district: str
    address_street: str
    address_number: str
    address_zipcode: str
    birthday: date


class UserFindAndUpdateRepository(BaseRepository):
    def update(self, params: UserFindAndUpdateRepositoryParams) -> User:
        getting_repository: IFindRepository[
            UserFindRepositoryParams, User
        ] = UserFindRepository(self.session)

        user: User = getting_repository.find_one(params)

        user.rg = CharUtils.keep_only_number(params.document_rg)
        user.cpf = CharUtils.keep_only_number(params.document)
        user.data_nascimento = params.birthday
        user.email = params.email.upper()
        user.nome = params.name.upper()
        user.telefone = CharUtils.keep_only_number(params.telephone)
        user.estado_emissor = params.state_issuer.upper()
        user.endereco_uf = params.address_state.upper()
        user.endereco_cidade = params.address_city.upper()
        user.endereco_bairro = params.address_district.upper()
        user.endereco_logradouro = params.address_street.upper()
        user.endereco_numero = CharUtils.keep_only_number(params.address_number)
        user.endereco_cep = CharUtils.keep_only_number(params.address_zipcode)

        self.session.add(user)

        return user
