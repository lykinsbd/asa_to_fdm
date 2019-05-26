# API Resources

from flask_restful import Resource
from asa_to_fdm import __version__


class HelloWorld(Resource):
    @staticmethod
    def get() -> dict:
        return {"hello": "world", "app": "asa_to_fdm", "version": __version__}
