"""
Payments Blueprint
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Order, Payment, Download, Product
from app.utils import send_purchase_confirmation_email
import stripe
import razorpay

payments_bp = Blueprint('payments', __name__)

# Initialize payment gateways
stripe.api_key = current_app.config.get('STRIPE_SECRET_KEY')


@payments_bp.route('/checkout/<int:order_id>')
@login_required
def checkout(order_id):
    """Checkout page."""
    order = Order.query.get_or_404(order_id)
    
    if order.buyer_id != current_user.id:
        flash('You do not have permission to checkout this order.', 'danger')
        return redirect(url_for('main.index'))
    
    if order.status != 'pending':
        flash('This order cannot be checked out.', 'warning')
        return redirect(url_for('orders.detail', order_id=order_id))
    
    return render_template('payments/checkout.html',
                         order=order,
                         stripe_public_key=current_app.config.get('STRIPE_PUBLIC_KEY'),
                         razorpay_key=current_app.config.get('RAZORPAY_KEY_ID'))


@payments_bp.route('/stripe/create-checkout-session/<int:order_id>', methods=['POST'])
@login_required
def stripe_create_session(order_id):
    """Create Stripe checkout session."""
    order = Order.query.get_or_404(order_id)
    
    if order.buyer_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        line_items = []
        for item in order.items:
            line_items.append({
                'price_data': {
                    'currency': 'inr',
                    'product_data': {
                        'name': item.product.title,
                        'description': item.product.description[:100],
                        'images': [f"{current_app.config.get('SITE_URL')}/static/uploads/{item.product.thumbnail}"],
                    },
                    'unit_amount': int(item.final_price * 100),
                },
                'quantity': 1,
            })
        
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=line_items,
            mode='payment',
            success_url=url_for('payments.stripe_success', order_id=order_id, _external=True),
            cancel_url=url_for('payments.checkout', order_id=order_id, _external=True),
            customer_email=current_user.email,
        )
        
        return jsonify({'sessionId': session.id})
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@payments_bp.route('/stripe/success/<int:order_id>')
@login_required
def stripe_success(order_id):
    """Stripe payment success."""
    order = Order.query.get_or_404(order_id)
    
    # Update order status
    order.status = 'completed'
    db.session.commit()
    
    # Create payment record
    payment = Payment(
        order_id=order.id,
        transaction_id=f"stripe-{order.order_number}",
        gateway='stripe',
        amount=order.final_amount,
        status='completed'
    )
    db.session.add(payment)
    db.session.commit()
    
    # Create download records
    for item in order.items:
        download = Download.create_for_order(
            current_user.id,
            item.product_id,
            order.id,
            max_downloads=-1,
            expiry_days=30
        )
        db.session.add(download)
    
    db.session.commit()
    
    # Send confirmation email
    send_purchase_confirmation_email(order)
    
    flash('Payment successful! Your products are ready to download.', 'success')
    return redirect(url_for('downloads.list'))


@payments_bp.route('/razorpay/create-order/<int:order_id>', methods=['POST'])
@login_required
def razorpay_create_order(order_id):
    """Create Razorpay order."""
    order = Order.query.get_or_404(order_id)
    
    if order.buyer_id != current_user.id:
        return jsonify({'error': 'Unauthorized'}), 403
    
    try:
        client = razorpay.Client(auth=(
            current_app.config.get('RAZORPAY_KEY_ID'),
            current_app.config.get('RAZORPAY_KEY_SECRET')
        ))
        
        razorpay_order = client.order.create({
            'amount': int(order.final_amount * 100),
            'currency': 'INR',
            'receipt': order.order_number,
            'notes': {
                'order_id': order.id,
                'email': current_user.email
            }
        })
        
        return jsonify({
            'razorpay_order_id': razorpay_order['id'],
            'amount': razorpay_order['amount'],
            'currency': razorpay_order['currency']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 400


@payments_bp.route('/razorpay/verify', methods=['POST'])
@login_required
def razorpay_verify():
    """Verify Razorpay payment."""
    try:
        order_id = request.form.get('order_id')
        payment_id = request.form.get('payment_id')
        signature = request.form.get('signature')
        
        order = Order.query.get_or_404(order_id)
        
        client = razorpay.Client(auth=(
            current_app.config.get('RAZORPAY_KEY_ID'),
            current_app.config.get('RAZORPAY_KEY_SECRET')
        ))
        
        # Verify payment signature
        params_dict = {'razorpay_order_id': order.order_number, 'razorpay_payment_id': payment_id, 'razorpay_signature': signature}
        client.utility.verify_payment_signature(params_dict)
        
        # Update order
        order.status = 'completed'
        payment = Payment(
            order_id=order.id,
            transaction_id=payment_id,
            gateway='razorpay',
            amount=order.final_amount,
            status='completed'
        )
        db.session.add(payment)
        db.session.commit()
        
        # Create downloads
        for item in order.items:
            download = Download.create_for_order(
                current_user.id,
                item.product_id,
                order.id
            )
            db.session.add(download)
        db.session.commit()
        
        send_purchase_confirmation_email(order)
        flash('Payment successful!', 'success')
        return redirect(url_for('downloads.list'))
    except:
        flash('Payment verification failed.', 'danger')
        return redirect(url_for('orders.detail', order_id=order_id))
