"""start instance of web server"""
import os

from src.web_server import create_app

app = create_app(os.environ["FLASK_CONFIG"])
