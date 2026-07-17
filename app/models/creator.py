"""
Creator Model
"""
from datetime import datetime
from app import db


class Creator(db.Model):
    """Creator profile model."""
    
    __tablename__ = 'creators'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True, index=True)
    display_name = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(120), unique=True, nullable=False, index=True)
    bio = db.Column(db.Text, nullable=True)
    cover_image = db.Column(db.String(255), nullable=True)
    profile_verified = db.Column(db.Boolean, default=False)
    website = db.Column(db.String(255), nullable=True)
    social_links = db.Column(db.JSON, default={})
    bank_account = db.Column(db.JSON, nullable=True)  # Encrypted bank details
    is_active = db.Column(db.Boolean, default=True)
    total_followers = db.Column(db.Integer, default=0)
    total_sales = db.Column(db.Float, default=0.0)
    total_revenue = db.Column(db.Float, default=0.0)
    total_downloads = db.Column(db.Integer, default=0)
    avg_rating = db.Column(db.Float, default=0.0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='creator', lazy='dynamic', cascade='all, delete-orphan')
    supporters = db.relationship('Support', backref='creator', lazy='dynamic', cascade='all, delete-orphan')
    memberships = db.relationship('Membership', backref='creator', lazy='dynamic', cascade='all, delete-orphan')
    messages_received = db.relationship('Message', foreign_keys='Message.creator_id', backref='creator', lazy='dynamic')
    
    def __repr__(self):
        return f'<Creator {self.display_name}>'
    
    def get_total_followers(self):
        """Get total followers count."""
        from app.models.follower import Follower
        return Follower.query.filter_by(following_id=self.user_id).count()
    
    def get_total_products(self):
        """Get total products count."""
        return Product.query.filter_by(creator_id=self.id, is_published=True).count()
    
    def get_total_earnings(self):
        """Get total earnings."""
        from app.models.payment import Payment
        payments = Payment.query.join(
            Order, Payment.order_id == Order.id
        ).filter(Order.creator_id == self.id, Payment.status == 'completed').all()
        return sum(p.amount for p in payments)
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'display_name': self.display_name,
            'slug': self.slug,
            'bio': self.bio,
            'cover_image': self.cover_image,
            'profile_verified': self.profile_verified,
            'website': self.website,
            'total_followers': self.total_followers,
            'total_sales': self.total_sales,
            'total_revenue': self.total_revenue,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
