import logging
from typing import Type

from pydantic import BaseModel

_logger = logging.getLogger(__name__)

class SessionFactory:
    def create_session(self, output_schema: Type[BaseModel] = None, temperature: float = 0):
        _logger.warning(
            "Trying to create a session with SessionFactory instance." 
            "Subclass this class and provide your own implementation of create_session.")