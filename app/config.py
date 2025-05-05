"""
Configuration settings for the Flask application
"""

# Swagger configuration
SWAGGER_TEMPLATE = {
    "swagger": "2.0",
    "info": {
        "title": "Flask-MVC PDF Embed/Extract API",
        "description": "API for embedding PDFs into a host PDF and extracting embedded PDFs",
        "version": "1.0.0",
        "contact": {
            "name": "API Support"
        }
    },
    "consumes": [
        "multipart/form-data"
    ],
    "produces": [
        "application/json",
        "application/pdf"
    ]
}