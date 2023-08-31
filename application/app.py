# import os
from flask import Flask
from flask_cors import CORS
from application.v1.route import v1_blueprint
import redis


def create_app():
    app = Flask(__name__)

    app.register_blueprint(v1_blueprint)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
