"""
Main Blueprint
"""
from flask import Blueprint, render_template, request
from app.models import Product, Category, Creator, User
from app.utils import paginate_query

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    """Home page."""
    featured_products = Product.query.filter_by(is_featured=True, is_published=True).limit(8).all()
    trending_products = Product.query.filter_by(is_published=True).order_by(Product.sales_count.desc()).limit(8).all()
    latest_products = Product.query.filter_by(is_published=True).order_by(Product.created_at.desc()).limit(8).all()
    categories = Category.query.filter_by(is_active=True).limit(10).all()
    
    return render_template('home.html',
                         featured_products=featured_products,
                         trending_products=trending_products,
                         latest_products=latest_products,
                         categories=categories)


@main_bp.route('/explore')
def explore():
    """Product exploration page."""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    category_id = request.args.get('category', 0, type=int)
    sort_by = request.args.get('sort', 'newest')
    min_price = request.args.get('min_price', 0, type=float)
    max_price = request.args.get('max_price', 999999, type=float)
    
    query = Product.query.filter_by(is_published=True)
    
    if search:
        query = query.filter(
            (Product.title.ilike(f'%{search}%')) |
            (Product.description.ilike(f'%{search}%')) |
            (Product.tags.ilike(f'%{search}%'))
        )
    
    if category_id:
        query = query.filter_by(category_id=category_id)
    
    query = query.filter(
        Product.price.between(min_price, max_price)
    )
    
    if sort_by == 'newest':
        query = query.order_by(Product.created_at.desc())
    elif sort_by == 'best_selling':
        query = query.order_by(Product.sales_count.desc())
    elif sort_by == 'highest_rated':
        query = query.order_by(Product.avg_rating.desc())
    elif sort_by == 'price_low':
        query = query.order_by(Product.price.asc())
    elif sort_by == 'price_high':
        query = query.order_by(Product.price.desc())
    
    products = paginate_query(query, page=page, per_page=12)
    categories = Category.query.filter_by(is_active=True).all()
    
    return render_template('explore.html',
                         products=products,
                         categories=categories,
                         search=search,
                         current_category=category_id,
                         sort_by=sort_by,
                         min_price=min_price,
                         max_price=max_price)


@main_bp.route('/creators')
def creators():
    """Creators listing page."""
    page = request.args.get('page', 1, type=int)
    search = request.args.get('search', '')
    sort_by = request.args.get('sort', 'followers')
    
    query = Creator.query.filter_by(is_active=True)
    
    if search:
        query = query.filter(
            (Creator.display_name.ilike(f'%{search}%')) |
            (Creator.bio.ilike(f'%{search}%'))
        )
    
    if sort_by == 'followers':
        query = query.order_by(Creator.total_followers.desc())
    elif sort_by == 'newest':
        query = query.order_by(Creator.created_at.desc())
    elif sort_by == 'earnings':
        query = query.order_by(Creator.total_revenue.desc())
    
    creators = paginate_query(query, page=page, per_page=12)
    
    return render_template('creators.html', creators=creators, search=search, sort_by=sort_by)


@main_bp.route('/about')
def about():
    """About page."""
    return render_template('about.html')


@main_bp.route('/faqs')
def faqs():
    """FAQs page."""
    return render_template('faqs.html')
