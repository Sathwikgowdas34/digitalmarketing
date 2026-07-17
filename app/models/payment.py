"""
Payment Model
"""
from datetime import datetime
from app import db


class Payment(db.Model):
    """Payment transaction model."""
    
    __tablename__ = 'payments'
    
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False, unique=True, index=True)
    transaction_id = db.Column(db.String(100), unique=True, nullable=False, index=True)
    gateway = db.Column(db.String(20), nullable=False)  # stripe, razorpay
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(10), default='INR')
    status = db.Column(db.String(20), default='pending')  # pending, completed, failed, refunded
    method = db.Column(db.String(50), nullable=True)  # card, upi, wallet, etc.
    gateway_response = db.Column(db.JSON, nullable=True)
    error_message = db.Column(db.Text, nullable=True)
    refund_amount = db.Column(db.Float, default=0)
    refund_reason = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Payment {self.transaction_id}>'
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'order_id': self.order_id,
            'transaction_id': self.transaction_id,
            'gateway': self.gateway,
            'amount': self.amount,
            'currency': self.currency,
            'status': self.status,
            'method': self.method,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
