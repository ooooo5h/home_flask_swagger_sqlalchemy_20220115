from http import server
from flask import Flask

def create_app(config_name):
    app = Flask(__name__)
    
    app.config.from_object(f'server.config.{config_name}')
    
    return app