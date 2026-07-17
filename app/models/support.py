"""
Support/Tip Model
"""
from datetime import datetime
from app import db


class Support(db.Model):
    """Creator support/tip transaction model."""
    
    __tablename__ = 'supports'
    
    id = db.Column(db.Integer, primary_key=True)
    supporter_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('creators.id'), nullable=False, index=True)
    amount = db.Column(db.Float, nullable=False)
    message = db.Column(db.Text, nullable=True)
    is_anonymous = db.Column(db.Boolean, default=False)
    display_on_wall = db.Column(db.Boolean, default=True)
    transaction_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    payment_status = db.Column(db.String(20), default='completed')
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    
    def __repr__(self):
        return f'<Support {self.amount} to creator {self.creator_id}>'
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'supporter': None if self.is_anonymous else self.supporter.to_dict(),
            'amount': self.amount,
            'message': self.message,
            'is_anonymous': self.is_anonymous,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
