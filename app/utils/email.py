"""
Email Utilities
"""
from flask_mail import Message
from flask import render_template_string, current_app
from app import mail
from threading import Thread


def send_async_email(app, msg):
    """Send email asynchronously."""
    with app.app_context():
        mail.send(msg)


def send_email(subject, recipients, text_body=None, html_body=None, sender=None):
    """Send email."""
    if sender is None:
        sender = current_app.config.get('MAIL_DEFAULT_SENDER')
    
    msg = Message(subject=subject, recipients=recipients, sender=sender)
    msg.body = text_body
    msg.html = html_body
    
    Thread(target=send_async_email, args=(current_app._get_current_object(), msg)).start()


def send_verification_email(user, verification_link):
    """Send email verification link."""
    subject = 'Verify Your Email - CreatorHub'
    html = f"""
    <h2>Welcome to CreatorHub!</h2>
    <p>Hi {user.get_full_name()},</p>
    <p>Please verify your email by clicking the link below:</p>
    <p><a href="{verification_link}" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Verify Email</a></p>
    <p>If you didn't create this account, please ignore this email.</p>
    """
    send_email(subject, [user.email], html_body=html)


def send_password_reset_email(user, reset_link):
    """Send password reset email."""
    subject = 'Reset Your Password - CreatorHub'
    html = f"""
    <h2>Password Reset Request</h2>
    <p>Hi {user.get_full_name()},</p>
    <p>We received a request to reset your password. Click the link below to proceed:</p>
    <p><a href="{reset_link}" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Reset Password</a></p>
    <p>This link will expire in 1 hour.</p>
    <p>If you didn't request this, please ignore this email.</p>
    """
    send_email(subject, [user.email], html_body=html)


def send_welcome_email(user):
    """Send welcome email."""
    subject = 'Welcome to CreatorHub!'
    html = f"""
    <h2>Welcome, {user.get_full_name()}!</h2>
    <p>Thank you for joining CreatorHub. We're excited to have you on board!</p>
    <p>Here's what you can do:</p>
    <ul>
        <li>Browse and purchase digital products from amazing creators</li>
        <li>Support your favorite creators</li>
        <li>Become a creator yourself and sell digital products</li>
        <li>Build a community of supporters</li>
    </ul>
    <p><a href="{current_app.config.get('SITE_URL')}" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Visit CreatorHub</a></p>
    """
    send_email(subject, [user.email], html_body=html)


def send_purchase_confirmation_email(order):
    """Send purchase confirmation email."""
    subject = f'Purchase Confirmation - Order {order.order_number}'
    items_html = ''
    for item in order.items:
        items_html += f"<tr><td>{item.product.title}</td><td>₹{item.final_price}</td></tr>"
    
    html = f"""
    <h2>Order Confirmation</h2>
    <p>Hi {order.buyer.get_full_name()},</p>
    <p>Thank you for your purchase!</p>
    <h3>Order Details</h3>
    <p><strong>Order Number:</strong> {order.order_number}</p>
    <p><strong>Total Amount:</strong> ₹{order.final_amount}</p>
    <table style="border-collapse: collapse; width: 100%;">
        <tr style="background-color: #f0f0f0;">
            <th style="border: 1px solid #ddd; padding: 8px;">Product</th>
            <th style="border: 1px solid #ddd; padding: 8px;">Price</th>
        </tr>
        {items_html}
    </table>
    <p><a href="{current_app.config.get('SITE_URL')}/downloads" style="background-color: #28a745; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Download Products</a></p>
    """
    send_email(subject, [order.buyer.email], html_body=html)


def send_support_confirmation_email(support):
    """Send support confirmation email."""
    subject = 'Thank You for Your Support!'
    supporter_name = support.supporter.get_full_name() if not support.is_anonymous else 'Anonymous'
    
    html = f"""
    <h2>Support Received!</h2>
    <p>Hi {support.creator.user.get_full_name()},</p>
    <p>You received a support of ₹{support.amount} from {supporter_name}!</p>
    {f'<p><strong>Message:</strong> {support.message}</p>' if support.message else ''}
    <p>Thank you for your work and keep creating amazing content!</p>
    """
    send_email(subject, [support.creator.user.email], html_body=html)


def send_membership_confirmation_email(user_membership):
    """Send membership confirmation email."""
    membership = user_membership.membership
    subject = f'Welcome to {membership.name} - CreatorHub'
    
    benefits_html = ''.join([f'<li>{benefit}</li>' for benefit in membership.benefits])
    
    html = f"""
    <h2>Membership Activated!</h2>
    <p>Hi {user_membership.user.get_full_name()},</p>
    <p>You've successfully subscribed to <strong>{membership.name}</strong>!</p>
    <h3>Benefits:</h3>
    <ul>
        {benefits_html}
    </ul>
    <p><a href="{current_app.config.get('SITE_URL')}/dashboard/memberships" style="background-color: #007bff; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Manage Subscription</a></p>
    """
    send_email(subject, [user_membership.user.email], html_body=html)
