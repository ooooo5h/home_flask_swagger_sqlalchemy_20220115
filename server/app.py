from distutils.command.config import config
from flask import Flask
from flask_restful_swagger_2 import Api
from flask_swagger_ui import get_swaggerui_blueprint

def create_app(config_name):
    app = Flask(__name__)
    
    app.config.from_object(f'server.config.{config_name}')
    
    api = Api(app, api_spec_url='/api/spec', title='my_server spec', api_version='0.1', catch_all_404s=True)
    
    

    from server.api.user import User
    from server.api.lecture import Lecture
    
    api.add_resource(User, '/user')
    api.add_resource(Lecture, '/lecture')
    
    
    swagger_ui = get_swaggerui_blueprint('/api/docs', '/api/spec.json', config={'app_name' : 'my sns service'})
    app.register_blueprint(swagger_ui, url_prefix='/api/docs')
    
    
    return app