"""
Review Model
"""
from datetime import datetime
from app import db


class Review(db.Model):
    """Product review and rating model."""
    
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, index=True)
    reviewer_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    title = db.Column(db.String(255), nullable=True)
    comment = db.Column(db.Text, nullable=True)
    is_verified_purchase = db.Column(db.Boolean, default=True)
    is_helpful_count = db.Column(db.Integer, default=0)
    is_unhelpful_count = db.Column(db.Integer, default=0)
    is_approved = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Review {self.product_id} - {self.rating} stars>'
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'product_id': self.product_id,
            'reviewer': self.reviewer.to_dict() if self.reviewer else None,
            'rating': self.rating,
            'title': self.title,
            'comment': self.comment,
            'is_verified_purchase': self.is_verified_purchase,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
