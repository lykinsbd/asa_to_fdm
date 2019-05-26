#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
 config.py
 Author: Brett Lykins (brett.lykins@rackspace.com)
 Description: Plumbs up our Flask app
"""

import os


from asa_to_fdm.library.error_handlers import ASAUnreachable
from flask import jsonify
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from flask.app import Flask


def app_configure(app: Flask) -> None:

    """
    Takes in an instantiated Flask instance and configures it.
    :param app:
    :return:
    """

    app.config.from_object(_DefaultSettings)

    if app.config["APP_ENVIRONMENT"].lower() == "dev":

        # Today we're not differentiating on environment...
        pass

    elif app.config["APP_ENVIRONMENT"].lower() == "staging":

        # Today we're not differentiating on environment...
        pass

    elif app.config["APP_ENVIRONMENT"].lower() == "production":

        # Today we're not differentiating on environment...
        pass

    api_key = os.environ.get("ASA_TO_FDM_API_KEY", None)

    # Stash the things we need later
    app.config.update({"API_KEY": api_key})

    # Register the error handlers
    @app.errorhandler(ASAUnreachable)
    def handle_asa_unreachable(error):
        response = jsonify(error.payload)
        response.status_code = error.status_code
        return response


class _DefaultSettings(object):
    """
    Set base variables based on deployment
    """

    LOG_LEVELS = {"CRITICAL": 50, "ERROR": 40, "WARNING": 30, "INFO": 20, "DEBUG": 10, "NOTSET": 0}
    VALID_ENVIRONMENTS = ["dev", "staging", "production"]

    APP_ENVIRONMENT = os.environ.get("APP_ENVIRONMENT", "dev")

    # Default set the env to "dev" if something invalid is specified"""
    if APP_ENVIRONMENT.lower() not in VALID_ENVIRONMENTS:
        APP_ENVIRONMENT = "dev"

    # Disable flask debugger
    DEBUG = False

    if "dev" in APP_ENVIRONMENT:
        LOG_LEVEL = LOG_LEVELS.get(os.environ.get("LOG_LEVEL", "DEBUG"), "DEBUG")
    else:
        LOG_LEVEL = LOG_LEVELS.get(os.environ.get("LOG_LEVEL", "INFO"), "INFO")

    JSON_SORT_KEYS = False
