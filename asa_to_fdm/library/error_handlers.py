#!/usr/bin/env python3
# -*- coding: UTF-8 -*-


from asa_to_fdm import __version__
from typing import Optional


class ASAToFDMBaseException(Exception):
    def __init__(self, message: str, status_code: Optional[int] = None, payload: Optional[dict] = None) -> None:

        super().__init__()

        self.message = message

        if status_code is not None:
            self.status_code = status_code

        if payload is None:
            self.payload = {}
        else:
            self.payload = payload

        self.payload["version"] = __version__
        self.payload["message"] = self.message


class ASAUnreachable(ASAToFDMBaseException):
    def __init__(self, message: Optional[str] = None, status_code: int = 504, payload: Optional[dict] = None) -> None:
        """
        Exception for if the ASA was unreachable in some way
        :param message:
        :param status_code: Defaults to 504
        :param payload:
        """

        if message is None:
            message = "Source ASA was unreachable."

        super().__init__(message=message, status_code=status_code, payload=payload)
