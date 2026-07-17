"""
Orders Blueprint
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models import Order, OrderItem, Product, Payment, Download, Coupon
from app.utils import generate_order_number
from datetime import datetime

orders_bp = Blueprint('orders', __name__)


@orders_bp.route('/create', methods=['POST'])
@login_required
def create():
    """Create new order."""
    product_ids = request.form.getlist('products')
    coupon_code = request.form.get('coupon_code', '').strip()
    
    if not product_ids:
        return jsonify({'status': 'error', 'message': 'No products selected'}), 400
    
    total_amount = 0
    discount_amount = 0
    items = []
    creator_id = None
    
    for product_id in product_ids:
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'status': 'error', 'message': 'Product not found'}), 404
        
        if not product.is_published:
            return jsonify({'status': 'error', 'message': 'Product is not available'}), 400
        
        creator_id = product.creator_id
        price = product.get_discounted_price()
        total_amount += price
        items.append({
            'product_id': product.id,
            'price': product.price,
            'discounted_price': price,
            'discount': product.discount_percentage
        })
    
    # Apply coupon if provided
    if coupon_code:
        coupon = Coupon.query.filter_by(code=coupon_code).first()
        if coupon and coupon.is_valid():
            discount_amount = coupon.calculate_discount(total_amount)
        else:
            return jsonify({'status': 'error', 'message': 'Invalid coupon code'}), 400
    
    # Create order
    order = Order(
        order_number=generate_order_number(),
        buyer_id=current_user.id,
        creator_id=creator_id,
        total_amount=total_amount,
        discount_amount=discount_amount,
        final_amount=total_amount - discount_amount,
        coupon_code=coupon_code
    )
    
    db.session.add(order)
    db.session.flush()
    
    # Add order items
    for item in items:
        order_item = OrderItem(
            order_id=order.id,
            product_id=item['product_id'],
            price=item['price'],
            discount=item['discount'],
            final_price=item['discounted_price']
        )
        db.session.add(order_item)
    
    db.session.commit()
    
    return jsonify({
        'status': 'success',
        'message': 'Order created',
        'order_id': order.id,
        'redirect': url_for('payments.checkout', order_id=order.id)
    })


@orders_bp.route('/<int:order_id>')
@login_required
def detail(order_id):
    """Order detail page."""
    order = Order.query.get_or_404(order_id)
    
    if order.buyer_id != current_user.id and not current_user.is_admin:
        flash('You do not have permission to view this order.', 'danger')
        return redirect(url_for('main.index'))
    
    return render_template('orders/detail.html', order=order)


@orders_bp.route('/my-orders')
@login_required
def my_orders():
    """User's orders page."""
    page = request.args.get('page', 1, type=int)
    orders = Order.query.filter_by(buyer_id=current_user.id).order_by(
        Order.created_at.desc()
    ).paginate(page=page, per_page=10, error_out=False)
    
    return render_template('orders/my_orders.html', orders=orders)
