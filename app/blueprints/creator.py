"""
Creator Blueprint
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from app import db
from app.models import User, Creator, Product
from app.utils import creator_required, generate_slug, save_picture

creator_bp = Blueprint('creator', __name__)


@creator_bp.route('/profile/<slug>')
def profile(slug):
    """Creator public profile."""
    creator = Creator.query.filter_by(slug=slug).first_or_404()
    page = request.args.get('page', 1, type=int)
    
    products = Product.query.filter_by(creator_id=creator.id, is_published=True).paginate(
        page=page, per_page=12, error_out=False
    )
    
    is_following = False
    if current_user.is_authenticated:
        is_following = current_user.is_following(creator.user)
    
    return render_template('creator/profile.html',
                         creator=creator,
                         products=products,
                         is_following=is_following)


@creator_bp.route('/apply', methods=['GET', 'POST'])
@login_required
def apply_creator():
    """Apply to become a creator."""
    if current_user.creator:
        flash('You are already a creator.', 'info')
        return redirect(url_for('creator.dashboard.index'))
    
    if request.method == 'POST':
        display_name = request.form.get('display_name', '').strip()
        bio = request.form.get('bio', '').strip()
        website = request.form.get('website', '').strip()
        
        if not display_name:
            flash('Display name is required.', 'danger')
            return redirect(url_for('creator.apply_creator'))
        
        slug = generate_slug(display_name)
        if Creator.query.filter_by(slug=slug).first():
            flash('This display name is already taken.', 'danger')
            return redirect(url_for('creator.apply_creator'))
        
        creator = Creator(
            user_id=current_user.id,
            display_name=display_name,
            slug=slug,
            bio=bio,
            website=website
        )
        
        db.session.add(creator)
        current_user.is_creator = True
        db.session.commit()
        
        flash('Welcome to CreatorHub! Your creator account is ready.', 'success')
        return redirect(url_for('dashboard.index'))
    
    return render_template('creator/apply.html')


@creator_bp.route('/follow/<int:creator_id>', methods=['POST'])
@login_required
def follow(creator_id):
    """Follow a creator."""
    creator = Creator.query.get_or_404(creator_id)
    current_user.follow(creator.user)
    db.session.commit()
    return {'status': 'success', 'message': 'Following creator'}


@creator_bp.route('/unfollow/<int:creator_id>', methods=['POST'])
@login_required
def unfollow(creator_id):
    """Unfollow a creator."""
    creator = Creator.query.get_or_404(creator_id)
    current_user.unfollow(creator.user)
    db.session.commit()
    return {'status': 'success', 'message': 'Unfollowed creator'}
