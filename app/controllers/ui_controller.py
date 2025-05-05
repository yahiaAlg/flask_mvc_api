"""
Controller for UI routes
"""
from flask import Blueprint, render_template

# Create blueprint
ui_bp = Blueprint('ui', __name__)


@ui_bp.route('/')
def index():
    """Simple UI for the PDF Embed/Extract API"""
    return render_template('pdf_embed_extract.html')