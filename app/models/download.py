"""
Download Model
"""
from datetime import datetime, timedelta
from app import db
import secrets


class Download(db.Model):
    """Download tracking and link generation model."""
    
    __tablename__ = 'downloads'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, index=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False, index=True)
    token = db.Column(db.String(100), unique=True, nullable=False, index=True)
    download_count = db.Column(db.Integer, default=0)
    max_downloads = db.Column(db.Integer, default=-1)  # -1 means unlimited
    expires_at = db.Column(db.DateTime, nullable=True)  # None means never expires
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_downloaded_at = db.Column(db.DateTime, nullable=True)
    
    def __repr__(self):
        return f'<Download {self.token}>'
    
    @staticmethod
    def generate_token():
        """Generate secure download token."""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def create_for_order(user_id, product_id, order_id, max_downloads=None, expiry_days=30):
        """Create download record for an order."""
        expires_at = datetime.utcnow() + timedelta(days=expiry_days) if expiry_days else None
        download = Download(
            user_id=user_id,
            product_id=product_id,
            order_id=order_id,
            token=Download.generate_token(),
            max_downloads=max_downloads if max_downloads else -1,
            expires_at=expires_at
        )
        return download
    
    def is_expired(self):
        """Check if download link is expired."""
        if self.expires_at and self.expires_at < datetime.utcnow():
            return True
        return False
    
    def can_download(self):
        """Check if download is allowed."""
        if not self.is_active:
            return False
        if self.is_expired():
            return False
        if self.max_downloads != -1 and self.download_count >= self.max_downloads:
            return False
        return True
    
    def record_download(self):
        """Record a download."""
        if self.can_download():
            self.download_count += 1
            self.last_downloaded_at = datetime.utcnow()
            return True
        return False
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'product_id': self.product_id,
            'token': self.token,
            'download_count': self.download_count,
            'max_downloads': self.max_downloads,
            'is_active': self.is_active,
            'is_expired': self.is_expired(),
            'can_download': self.can_download(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
