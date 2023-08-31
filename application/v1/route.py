from flask import Blueprint
from flask_restx import Api

from application.v1.resources.metar_handler.api import WeatherInfo

v1_blueprint = Blueprint(name="v1", import_name=__name__)

v1_api = Api(
    app=v1_blueprint,
    # prefix="/v1",
    title="Wheather services",
    version="1.0",
    description="Wheather Apis API",
    doc="/apidocs/",
)

# defining route
v1_api.add_resource(WeatherInfo, '/metar/info/')