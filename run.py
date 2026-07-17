"""
Application Entry Point
"""
import os
import logging
from logging.handlers import RotatingFileHandler
from app import create_app, db
from app.models import (
    User, Creator, Product, Category, Order, Payment, 
    Download, Review, Follower, Membership, Coupon, 
    Notification, Message, Support
)

# Create Flask application
app = create_app(os.getenv('FLASK_ENV', 'development'))

# Setup logging
if not app.debug and not app.testing:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    
    file_handler = RotatingFileHandler('logs/creatorhub.log', maxBytes=10240000, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('CreatorHub startup')


@app.shell_context_processor
def make_shell_context():
    """Create shell context for Flask CLI."""
    return {
        'db': db,
        'User': User,
        'Creator': Creator,
        'Product': Product,
        'Category': Category,
        'Order': Order,
        'Payment': Payment,
        'Download': Download,
        'Review': Review,
        'Follower': Follower,
        'Membership': Membership,
        'Coupon': Coupon,
        'Notification': Notification,
        'Message': Message,
        'Support': Support,
    }


if __name__ == '__main__':
    app.run()
