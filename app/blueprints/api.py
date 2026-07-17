"""
API Blueprint - placeholder for REST API
"""
from flask import Blueprint

api_bp = Blueprint('api', __name__)

@api_bp.route('/health')
def health():
    return {'status': 'ok'}
