"""
User Model
"""
from datetime import datetime
from app import db, bcrypt, login_manager
from flask_login import UserMixin


class User(UserMixin, db.Model):
    """User model for authentication and profile management."""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(120), nullable=True)
    last_name = db.Column(db.String(120), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    profile_image = db.Column(db.String(255), nullable=True)
    bio = db.Column(db.Text, nullable=True)
    is_verified = db.Column(db.Boolean, default=False)
    is_creator = db.Column(db.Boolean, default=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    email_notifications = db.Column(db.Boolean, default=True)
    newsletter_subscription = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_login = db.Column(db.DateTime, nullable=True)
    
    # Relationships
    creator = db.relationship('Creator', backref='user', uselist=False, cascade='all, delete-orphan')
    orders = db.relationship('Order', backref='buyer', lazy='dynamic', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='reviewer', lazy='dynamic', cascade='all, delete-orphan')
    downloads = db.relationship('Download', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    followers = db.relationship('Follower', foreign_keys='Follower.follower_id', backref='follower_user', lazy='dynamic')
    following = db.relationship('Follower', foreign_keys='Follower.following_id', backref='following_user', lazy='dynamic')
    wishlists = db.relationship('Product', secondary='wishlist', backref='wishlisted_by')
    messages = db.relationship('Message', backref='sender', lazy='dynamic', cascade='all, delete-orphan')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    supports = db.relationship('Support', backref='supporter', lazy='dynamic', cascade='all, delete-orphan')
    memberships = db.relationship('UserMembership', backref='user', lazy='dynamic', cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    def set_password(self, password):
        """Hash and set password."""
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        """Check password against hash."""
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def get_full_name(self):
        """Get user's full name."""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def is_following(self, user):
        """Check if user is following another user."""
        return self.following.filter_by(following_id=user.id).first() is not None
    
    def follow(self, user):
        """Follow a user."""
        if not self.is_following(user):
            follow = Follower(follower_id=self.id, following_id=user.id)
            db.session.add(follow)
    
    def unfollow(self, user):
        """Unfollow a user."""
        follow = self.following.filter_by(following_id=user.id).first()
        if follow:
            db.session.delete(follow)
    
    def add_to_wishlist(self, product):
        """Add product to wishlist."""
        if product not in self.wishlists:
            self.wishlists.append(product)
    
    def remove_from_wishlist(self, product):
        """Remove product from wishlist."""
        if product in self.wishlists:
            self.wishlists.remove(product)
    
    def is_in_wishlist(self, product):
        """Check if product is in wishlist."""
        return product in self.wishlists
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'full_name': self.get_full_name(),
            'phone': self.phone,
            'profile_image': self.profile_image,
            'bio': self.bio,
            'is_verified': self.is_verified,
            'is_creator': self.is_creator,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


wishlist = db.Table(
    'wishlist',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('product_id', db.Integer, db.ForeignKey('products.id'), primary_key=True)
)


@login_manager.user_loader
def load_user(user_id):
    """Load user by ID for Flask-Login."""
    return User.query.get(int(user_id))
