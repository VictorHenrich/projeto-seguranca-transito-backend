from typing import Union, Mapping, Any, List
from decimal import Decimal
from dataclasses import dataclass
import requests


@dataclass
class GeocodingPayload:
    zipcode: str
    state: str
    city: str
    district: str
    street: str


class GeocodingService:
    __url: str = "https://nominatim.openstreetmap.org/reverse"

    def __init__(self, lat: Union[str, float], lon: Union[str, float]) -> None:
        self.__lat: Decimal = Decimal(lat)
        self.__lon: Decimal = Decimal(lon)

    def __handle_state(self, state: str) -> str:
        first_word, last_word = state.split(" ")

        return f"{first_word[0]}{last_word[0]}".upper()

    def execute(self) -> GeocodingPayload:
        response: requests.Response = requests.get(
            GeocodingService.__url,
            params={"lat": str(self.__lat), "lon": str(self.__lon), "format": "jsonv2"},
        )

        if response.status_code >= 400:
            raise Exception(
                "Falha ao localiar endereço!\n", f"RESPONSE: {response.content}"
            )

        address_data: Mapping[str, Any] = response.json()

        return GeocodingPayload(
            address_data["address"]["postcode"],
            self.__handle_state(address_data["address"]["state"]),
            address_data["address"]["town"],
            address_data["address"]["suburb"],
            address_data["address"]["road"],
        )