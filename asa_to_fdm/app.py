#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""
 app.py
 Author: Brett Lykins (lykinsbd@gmail.com)
 Description: Main app setup/config
"""

import logging

from flask import Flask
from flask_restful import Api
from asa_to_fdm.resources.root import HelloWorld
from asa_to_fdm.resources.healthcheck import HealthCheck
from asa_to_fdm.config import app_configure


app = Flask(__name__)

# Setup your app
app_configure(app)

# Setup logging:
logger = logging.getLogger("asa_to_fdm")
logger.propagate = False  # fix duplicate messages
if not logger.handlers:
    logger.setLevel(logging.INFO)
    stderr_handler = logging.StreamHandler()
    normal_formatter = logging.Formatter("%(levelname)s - %(message)s")
    stderr_handler.setFormatter(normal_formatter)
    logger.addHandler(stderr_handler)

# Instantiate your API
api = Api(app, catch_all_404s=True)

# Add resources (wrappers for Flask views)
api.add_resource(HelloWorld, "/")
api.add_resource(HealthCheck, "/healthcheck/")
