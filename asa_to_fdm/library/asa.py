"""
Module to handle gathering/parsing ASA configuration into objects.
"""

import re
import requests

from ciscoconfparse import CiscoConfParse
from requests import RequestException
from typing import Optional


class ASA(object):
    """
    Object for representing a Cisco ASA.
    """

    def __init__(
        self,
        config: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[int] = 443,
        username: Optional[str] = None,
        password: Optional[str] = None,
    ) -> None:
        """
        Instantiate an ASA object, either by providing configuration, or connection information.

        Gathering the information requires user/password and an HTTPS connection to the ASA.
        """

        # Input validation
        if config is None and host is None:
            raise ValueError("Must provide either config or host!")
        if host is not None and (username is None or password is None):
            raise ValueError("Must provide credentials!")

        if config is None:
            try:
                resp = requests.get(
                    url=f"https://{host}:{port}/admin/exec/show+run+all",
                    auth=(username, password),
                    headers={"User-Agent": "ASDM"},
                    verify=False,
                )
            except RequestException:
                raise ConnectionError(
                    f"Unable to gather configuration from ASA {username}@{host}:{port}."
                )

            if resp.ok:
                config = resp.text
            else:
                raise ConnectionError(
                    f"Unable to gather configuration from ASA {username}@{host}:{port}."
                )

        self.raw_config = config
        self.parsed_config = CiscoConfParse(config=config.splitlines(), syntax="asa")
