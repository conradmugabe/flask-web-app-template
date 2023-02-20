"""create instance of flask web app"""
from flask import Flask


def create_app(config_name: str) -> Flask:
    """create instance of flask web app"""
    app = Flask(__name__)

    config_module = f"src.config.{config_name.capitalize()}Config"

    app.config.from_object(config_module)

    @app.route("/")
    def hello_world():
        return "Hello, World!"

    return app
