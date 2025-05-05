"""
Flask application factory
"""
# Apply patch for flasgger to work with Python 3.12
from app.flasgger_patch import *
from flask import Flask
from flasgger import Swagger
from app.controllers.pdf_controller import pdf_bp
from app.controllers.ui_controller import ui_bp


def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Configure Swagger
    swagger_config = {
        "headers": [],
        "specs": [
            {
                "endpoint": "apispec",
                "route": "/apispec.json",
                "rule_filter": lambda rule: True,
                "model_filter": lambda tag: True,
            }
        ],
        "static_url_path": "/flasgger_static",
        "swagger_ui": True,
        "specs_route": "/apidocs/"
    }
    
    swagger = Swagger(app, config=swagger_config)
    
    # Register blueprints
    app.register_blueprint(pdf_bp)
    app.register_blueprint(ui_bp)
    
    return app