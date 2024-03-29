from typing import IO
from uuid import UUID

from flask import Response
from server import HttpServer
from server.http import HttpController, ResponseIO
from services.attachment import AttachmentGettingService
from patterns.service import IService


@HttpServer.add_controller("/occurrence/attachment/query/<uuid:attachment_hash>")
class AttachmentQueryController(HttpController):
    def get(self, attachment_hash: UUID) -> Response:
        attachment_getting_service: IService[IO] = AttachmentGettingService(
            str(attachment_hash)
        )

        file: IO = attachment_getting_service.execute()

        return ResponseIO(file.name, file)
