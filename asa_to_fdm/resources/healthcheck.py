# API Resources

from flask_restful import Resource
from asa_to_fdm import __version__


class HealthCheck(Resource):
    @staticmethod
    def get() -> dict:
        return {"status": "OK", "app": "asa_to_fdm", "version": __version__}
