"""
Coupon Model
"""
from datetime import datetime
from app import db


class Coupon(db.Model):
    """Discount coupon model."""
    
    __tablename__ = 'coupons'
    
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('creators.id'), nullable=False, index=True)
    code = db.Column(db.String(50), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    discount_type = db.Column(db.String(20), default='percentage')  # percentage, fixed
    discount_value = db.Column(db.Float, nullable=False)
    max_uses = db.Column(db.Integer, nullable=True)  # None means unlimited
    current_uses = db.Column(db.Integer, default=0)
    min_purchase_amount = db.Column(db.Float, default=0)
    is_active = db.Column(db.Boolean, default=True)
    starts_at = db.Column(db.DateTime, nullable=True)
    expires_at = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', secondary='coupon_products', backref='coupons')
    
    def __repr__(self):
        return f'<Coupon {self.code}>'
    
    def is_valid(self):
        """Check if coupon is valid."""
        if not self.is_active:
            return False
        if self.starts_at and self.starts_at > datetime.utcnow():
            return False
        if self.expires_at and self.expires_at < datetime.utcnow():
            return False
        if self.max_uses and self.current_uses >= self.max_uses:
            return False
        return True
    
    def calculate_discount(self, amount):
        """Calculate discount amount."""
        if amount < self.min_purchase_amount:
            return 0
        
        if self.discount_type == 'percentage':
            return amount * (self.discount_value / 100)
        else:  # fixed
            return min(self.discount_value, amount)
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'code': self.code,
            'description': self.description,
            'discount_type': self.discount_type,
            'discount_value': self.discount_value,
            'is_valid': self.is_valid(),
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


coupon_products = db.Table(
    'coupon_products',
    db.Column('coupon_id', db.Integer, db.ForeignKey('coupons.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True)
)
