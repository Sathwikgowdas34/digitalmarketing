"""
Product and Category Models
"""
from datetime import datetime
from app import db


class Category(db.Model):
    """Product category model."""
    
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False, index=True)
    slug = db.Column(db.String(120), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=True)
    icon = db.Column(db.String(50), nullable=True)  # Font Awesome icon
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    products = db.relationship('Product', backref='category', lazy='dynamic')
    
    def __repr__(self):
        return f'<Category {self.name}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'slug': self.slug,
            'description': self.description,
        }


class Product(db.Model):
    """Digital product model."""
    
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('creators.id'), nullable=False, index=True)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'), nullable=False, index=True)
    title = db.Column(db.String(255), nullable=False, index=True)
    slug = db.Column(db.String(255), unique=True, nullable=False, index=True)
    description = db.Column(db.Text, nullable=False)
    features = db.Column(db.JSON, default=[])
    price = db.Column(db.Float, nullable=False)
    discount_percentage = db.Column(db.Float, default=0)
    thumbnail = db.Column(db.String(255), nullable=False)
    gallery = db.Column(db.JSON, default=[])
    preview_pdf = db.Column(db.String(255), nullable=True)
    file_path = db.Column(db.String(255), nullable=False)  # Path to uploaded file
    file_size = db.Column(db.Float, nullable=False)  # In MB
    file_type = db.Column(db.String(20), nullable=False)  # pdf, zip, epub, etc.
    version = db.Column(db.String(50), nullable=True)
    license = db.Column(db.String(50), nullable=True)
    release_notes = db.Column(db.Text, nullable=True)
    tags = db.Column(db.JSON, default=[])
    is_published = db.Column(db.Boolean, default=False, index=True)
    is_featured = db.Column(db.Boolean, default=False)
    rating_count = db.Column(db.Integer, default=0)
    total_rating = db.Column(db.Float, default=0.0)
    avg_rating = db.Column(db.Float, default=0.0)
    sales_count = db.Column(db.Integer, default=0)
    total_downloads = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    orders = db.relationship('OrderItem', backref='product', lazy='dynamic', cascade='all, delete-orphan')
    reviews = db.relationship('Review', backref='product', lazy='dynamic', cascade='all, delete-orphan')
    downloads = db.relationship('Download', backref='product', lazy='dynamic', cascade='all, delete-orphan')
    coupons = db.relationship('Coupon', secondary='coupon_products', backref='products')
    
    def __repr__(self):
        return f'<Product {self.title}>'
    
    def get_discounted_price(self):
        """Get price after discount."""
        if self.discount_percentage > 0:
            return self.price * (1 - self.discount_percentage / 100)
        return self.price
    
    def add_rating(self, rating):
        """Add a rating to the product."""
        self.total_rating += rating
        self.rating_count += 1
        self.avg_rating = self.total_rating / self.rating_count
    
    def to_dict(self):
        """Convert to dictionary."""
        return {
            'id': self.id,
            'title': self.title,
            'slug': self.slug,
            'description': self.description,
            'price': self.price,
            'discount_percentage': self.discount_percentage,
            'discounted_price': self.get_discounted_price(),
            'thumbnail': self.thumbnail,
            'category': self.category.to_dict() if self.category else None,
            'creator': self.creator.to_dict() if self.creator else None,
            'avg_rating': self.avg_rating,
            'rating_count': self.rating_count,
            'sales_count': self.sales_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
