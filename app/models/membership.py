"""
Membership Model
"""
from datetime import datetime, timedelta
from app import db


class Membership(db.Model):
    """Creator membership plan model."""
    
    __tablename__ = 'memberships'
    
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('creators.id'), nullable=False, index=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    billing_cycle = db.Column(db.String(20), default='monthly')  # monthly, yearly
    benefits = db.Column(db.JSON, default=[])
    max_members = db.Column(db.Integer, nullable=True)  # None means unlimited
    current_members = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    subscribers = db.relationship('UserMembership', backref='membership', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Membership {self.name}>'
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'price': self.price,
            'billing_cycle': self.billing_cycle,
            'benefits': self.benefits,
            'current_members': self.current_members,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class UserMembership(db.Model):
    """User membership subscription model."""
    
    __tablename__ = 'user_memberships'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    membership_id = db.Column(db.Integer, db.ForeignKey('memberships.id'), nullable=False, index=True)
    status = db.Column(db.String(20), default='active')  # active, cancelled, expired
    started_at = db.Column(db.DateTime, default=datetime.utcnow)
    expires_at = db.Column(db.DateTime, nullable=True)
    auto_renew = db.Column(db.Boolean, default=True)
    last_payment_date = db.Column(db.DateTime, nullable=True)
    next_payment_date = db.Column(db.DateTime, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<UserMembership {self.user_id} - {self.membership_id}>'
    
    def is_active_subscription(self):
        """Check if subscription is active."""
        if self.status != 'active':
            return False
        if self.expires_at and self.expires_at < datetime.utcnow():
            return False
        return True
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'membership': self.membership.to_dict() if self.membership else None,
            'status': self.status,
            'is_active': self.is_active_subscription(),
            'started_at': self.started_at.isoformat() if self.started_at else None,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
        }
