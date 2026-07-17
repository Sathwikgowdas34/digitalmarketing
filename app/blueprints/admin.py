"""
Admin Blueprint - placeholder for admin panel
"""
from flask import Blueprint

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/')
def index():
    return "Admin panel coming soon"
