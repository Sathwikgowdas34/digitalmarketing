"""
Flask Application Factory
"""
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_mail import Mail
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_caching import Cache
from flask_talisman import Talisman
from config import config

# Initialize extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()
mail = Mail()
limiter = Limiter(key_func=get_remote_address)
cache = Cache()
talisman = Talisman()


def create_app(config_name='development'):
    """
    Application factory
    """
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)
    mail.init_app(app)
    limiter.init_app(app)
    cache.init_app(app)
    talisman.init_app(app)
    
    # Login manager configuration
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # Create instance folder
    import os
    try:
        os.makedirs(app.instance_path, exist_ok=True)
        os.makedirs(os.path.join(app.instance_path, 'uploads'), exist_ok=True)
        os.makedirs('logs', exist_ok=True)
    except OSError:
        pass
    
    # Register blueprints
    register_blueprints(app)
    
    # Register error handlers
    register_error_handlers(app)
    
    # Register template filters and context processors
    register_template_utilities(app)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app


def register_blueprints(app):
    """
    Register Flask blueprints
    """
    from app.blueprints.auth import auth_bp
    from app.blueprints.main import main_bp
    from app.blueprints.creator import creator_bp
    from app.blueprints.products import products_bp
    from app.blueprints.orders import orders_bp
    from app.blueprints.payments import payments_bp
    from app.blueprints.downloads import downloads_bp
    from app.blueprints.dashboard import dashboard_bp
    from app.blueprints.admin import admin_bp
    from app.blueprints.api import api_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(creator_bp, url_prefix='/creator')
    app.register_blueprint(products_bp, url_prefix='/products')
    app.register_blueprint(orders_bp, url_prefix='/orders')
    app.register_blueprint(payments_bp, url_prefix='/payments')
    app.register_blueprint(downloads_bp, url_prefix='/downloads')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api_bp, url_prefix='/api')


def register_error_handlers(app):
    """
    Register error handlers
    """
    @app.errorhandler(404)
    def not_found(error):
        return {
            'error': 'Not Found',
            'status': 404,
            'message': 'The requested resource was not found.'
        }, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        db.session.rollback()
        return {
            'error': 'Internal Server Error',
            'status': 500,
            'message': 'An unexpected error occurred.'
        }, 500
    
    @app.errorhandler(403)
    def forbidden(error):
        return {
            'error': 'Forbidden',
            'status': 403,
            'message': 'You do not have permission to access this resource.'
        }, 403


def register_template_utilities(app):
    """
    Register template filters and context processors
    """
    from datetime import datetime
    
    @app.template_filter('currency')
    def currency_filter(value):
        """Format value as currency"""
        try:
            return f"₹{float(value):,.2f}"
        except:
            return value
    
    @app.template_filter('date_format')
    def date_format_filter(value, format='%d %b %Y'):
        """Format date"""
        if isinstance(value, datetime):
            return value.strftime(format)
        return value
    
    @app.template_filter('truncate')
    def truncate_filter(value, length=100):
        """Truncate text"""
        if len(value) > length:
            return value[:length] + '...'
        return value
    
    @app.context_processor
    def inject_user():
        """Inject current user into context"""
        from flask_login import current_user
        return {'current_user': current_user}
