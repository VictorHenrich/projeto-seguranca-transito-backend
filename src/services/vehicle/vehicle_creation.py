from typing import Optional
from dataclasses import dataclass
from sqlalchemy.orm import Session

from server import Databases
from models import User
from patterns.repository import ICreateRepository
from repositories.vehicle import (
    VehicleCreateRepository,
    VehicleCreateRepositoryParams,
)
from src.utils.entities import VehiclePayload
from utils.types import VehicleTypes


@dataclass
class VehicleCreateRepoProps:
    user: User
    plate: str
    renavam: str
    vehicle_type: VehicleTypes
    brand: Optional[str] = None
    model: Optional[str] = None
    color: Optional[str] = None
    year: Optional[int] = None
    chassi: Optional[str] = None
    have_safe: bool = False


class VehicleCreationService:
    def __init__(
        self,
        user: User,
        vehicle_payload: VehiclePayload,
        session: Optional[Session] = None,
    ) -> None:
        self.__props: VehicleCreateRepoProps = VehicleCreateRepoProps(
            user,
            vehicle_payload.plate,
            vehicle_payload.renavam,
            vehicle_payload.vehicle_type,
            vehicle_payload.brand,
            vehicle_payload.model,
            vehicle_payload.color,
            vehicle_payload.year,
            vehicle_payload.chassi,
            vehicle_payload.have_safe,
        )

        self.__session: Optional[Session] = session

    def __create_vehicle(self, session: Session) -> None:
        vehicle_create_repository: ICreateRepository[
            VehicleCreateRepositoryParams, None
        ] = VehicleCreateRepository(session)

        vehicle_create_repository.create(self.__props)

    def execute(self) -> None:
        if self.__session:
            self.__create_vehicle(self.__session)

        else:
            with Databases.create_session() as session:
                self.__create_vehicle(session)

                session.commit()
