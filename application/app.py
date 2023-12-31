from flask import Flask
from application.v1.route import v1_blueprint


def create_app():
    app = Flask(__name__)

    app.register_blueprint(v1_blueprint)

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
