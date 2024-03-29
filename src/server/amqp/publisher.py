from pika import ConnectionParameters, BasicProperties
from pika.adapters.blocking_connection import BlockingChannel
import logging

from .abstract_amqp import AbstractAMQP
from utils.types import DictType


class AMQPPublisher(AbstractAMQP):
    def __init__(
        self,
        publisher_name: str,
        connection: ConnectionParameters,
        exchange: str,
        body: bytes,
        routing_key: str,
        properties: DictType,
    ) -> None:
        super().__init__(connection)

        self.__publisher_name: str = publisher_name
        self.__exchange: str = exchange
        self.__body: bytes = body
        self.__routing_key: str = routing_key
        self.__properties: BasicProperties = BasicProperties(**properties)

    def start(self) -> None:
        channel: BlockingChannel = self.get_channel()

        channel.basic_publish(
            exchange=self.__exchange,
            body=self.__body,
            routing_key=self.__routing_key,
            properties=self.__properties,
        )

        logging.info(f"Publisher {self.__publisher_name} triggered an event!")
