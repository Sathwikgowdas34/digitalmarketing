"""
Downloads Blueprint
"""
from flask import Blueprint, render_template, request, send_file, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from app import db
from app.models import Download, Order
import os

downloads_bp = Blueprint('downloads', __name__)


@downloads_bp.route('/')
@login_required
def list():
    """List user's downloads."""
    page = request.args.get('page', 1, type=int)
    downloads = Download.query.filter_by(user_id=current_user.id).order_by(
        Download.created_at.desc()
    ).paginate(page=page, per_page=20, error_out=False)
    
    return render_template('downloads/list.html', downloads=downloads)


@downloads_bp.route('/<token>')
def download(token):
    """Download product using token."""
    download_record = Download.query.filter_by(token=token).first_or_404()
    
    if not download_record.can_download():
        flash('Download link is expired or maximum downloads exceeded.', 'danger')
        return redirect(url_for('main.index'))
    
    product = download_record.product
    file_path = os.path.join(current_app.instance_path, product.file_path)
    
    if not os.path.exists(file_path):
        flash('File not found.', 'danger')
        return redirect(url_for('main.index'))
    
    # Record download
    download_record.record_download()
    product.total_downloads += 1
    db.session.commit()
    
    return send_file(
        file_path,
        as_attachment=True,
        download_name=product.title + os.path.splitext(file_path)[1]
    )
