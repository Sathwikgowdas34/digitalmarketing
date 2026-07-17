"""
Products Blueprint
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import Product, Review, Order, OrderItem
from app.utils import paginate_query

products_bp = Blueprint('products', __name__)


@products_bp.route('/<slug>')
def detail(slug):
    """Product detail page."""
    product = Product.query.filter_by(slug=slug).first_or_404()
    
    if not product.is_published and (not current_user.is_authenticated or 
        (product.creator_id != current_user.creator.id if current_user.creator else True)):
        redirect(url_for('main.index'))
    
    page = request.args.get('page', 1, type=int)
    reviews = Review.query.filter_by(product_id=product.id, is_approved=True).paginate(
        page=page, per_page=10, error_out=False
    )
    
    related_products = Product.query.filter_by(
        category_id=product.category_id,
        is_published=True
    ).filter(Product.id != product.id).limit(6).all()
    
    is_in_wishlist = False
    has_purchased = False
    if current_user.is_authenticated:
        is_in_wishlist = current_user.is_in_wishlist(product)
        has_purchased = Order.query.join(OrderItem).filter(
            OrderItem.product_id == product.id,
            Order.buyer_id == current_user.id,
            Order.status == 'completed'
        ).first() is not None
    
    return render_template('products/detail.html',
                         product=product,
                         reviews=reviews,
                         related_products=related_products,
                         is_in_wishlist=is_in_wishlist,
                         has_purchased=has_purchased)


@products_bp.route('/<int:product_id>/wishlist', methods=['POST'])
@login_required
def toggle_wishlist(product_id):
    """Add/remove product from wishlist."""
    product = Product.query.get_or_404(product_id)
    
    if current_user.is_in_wishlist(product):
        current_user.remove_from_wishlist(product)
        message = 'Removed from wishlist'
    else:
        current_user.add_to_wishlist(product)
        message = 'Added to wishlist'
    
    db.session.commit()
    return {'status': 'success', 'message': message}


@products_bp.route('/<int:product_id>/review', methods=['POST'])
@login_required
def add_review(product_id):
    """Add product review."""
    product = Product.query.get_or_404(product_id)
    
    rating = request.form.get('rating', type=int)
    title = request.form.get('title', '').strip()
    comment = request.form.get('comment', '').strip()
    
    if not rating or rating < 1 or rating > 5:
        flash('Invalid rating.', 'danger')
        return redirect(url_for('products.detail', slug=product.slug))
    
    # Check if user has already reviewed
    existing_review = Review.query.filter_by(
        product_id=product_id,
        reviewer_id=current_user.id
    ).first()
    
    if existing_review:
        flash('You have already reviewed this product.', 'warning')
        return redirect(url_for('products.detail', slug=product.slug))
    
    review = Review(
        product_id=product_id,
        reviewer_id=current_user.id,
        rating=rating,
        title=title,
        comment=comment
    )
    
    product.add_rating(rating)
    db.session.add(review)
    db.session.commit()
    
    flash('Review added successfully!', 'success')
    return redirect(url_for('products.detail', slug=product.slug))
