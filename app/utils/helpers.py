"""
Helper Functions
"""
import os
import secrets
from datetime import datetime, timedelta
from PIL import Image
from app import current_app
import string


def allowed_file(filename, allowed_extensions=None):
    """Check if file extension is allowed."""
    if allowed_extensions is None:
        allowed_extensions = current_app.config.get('ALLOWED_EXTENSIONS', set())
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions


def save_uploaded_file(file, folder='uploads'):
    """Save uploaded file to instance folder."""
    if not file or file.filename == '':
        return None
    
    if not allowed_file(file.filename):
        return None
    
    # Generate unique filename
    ext = file.filename.rsplit('.', 1)[1].lower()
    filename = f"{secrets.token_hex(8)}.{ext}"
    
    # Create folder if not exists
    folder_path = os.path.join(current_app.instance_path, folder)
    os.makedirs(folder_path, exist_ok=True)
    
    file_path = os.path.join(folder_path, filename)
    file.save(file_path)
    
    return os.path.join(folder, filename)


def save_picture(form_picture, folder='profile_pics', size=(200, 200)):
    """Save and resize picture."""
    if not form_picture or form_picture.filename == '':
        return None
    
    ext = form_picture.filename.rsplit('.', 1)[1].lower()
    filename = f"{secrets.token_hex(8)}.{ext}"
    
    folder_path = os.path.join(current_app.instance_path, folder)
    os.makedirs(folder_path, exist_ok=True)
    
    file_path = os.path.join(folder_path, filename)
    
    # Resize image
    try:
        img = Image.open(form_picture)
        img.thumbnail(size)
        img.save(file_path)
    except Exception as e:
        current_app.logger.error(f"Error saving image: {e}")
        form_picture.save(file_path)
    
    return os.path.join(folder, filename)


def delete_file(file_path):
    """Delete file from filesystem."""
    try:
        full_path = os.path.join(current_app.instance_path, file_path)
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
    except Exception as e:
        current_app.logger.error(f"Error deleting file: {e}")
    return False


def format_currency(amount, currency='₹'):
    """Format amount as currency."""
    return f"{currency}{amount:,.2f}"


def generate_order_number():
    """Generate unique order number."""
    timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
    random_suffix = secrets.token_hex(4).upper()
    return f"ORD-{timestamp}-{random_suffix}"


def generate_slug(text):
    """Generate URL slug from text."""
    import re
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.rstrip('-')


def get_file_size(file_path):
    """Get file size in MB."""
    try:
        size_bytes = os.path.getsize(file_path)
        size_mb = size_bytes / (1024 * 1024)
        return round(size_mb, 2)
    except:
        return 0


def truncate_text(text, length=100, suffix='...'):
    """Truncate text to specified length."""
    if len(text) > length:
        return text[:length].rsplit(' ', 1)[0] + suffix
    return text


def generate_token(length=32):
    """Generate secure random token."""
    return secrets.token_urlsafe(length)


def get_password_strength(password):
    """Check password strength."""
    strength = 0
    if len(password) >= 8:
        strength += 1
    if any(c.isupper() for c in password):
        strength += 1
    if any(c.islower() for c in password):
        strength += 1
    if any(c.isdigit() for c in password):
        strength += 1
    if any(c in string.punctuation for c in password):
        strength += 1
    
    strength_levels = ['Very Weak', 'Weak', 'Fair', 'Good', 'Strong', 'Very Strong']
    return strength_levels[strength]


def validate_email_format(email):
    """Validate email format."""
    import re
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None


def get_time_ago(dt):
    """Get human-readable time difference."""
    if not dt:
        return 'Unknown'
    
    diff = datetime.utcnow() - dt
    seconds = diff.total_seconds()
    
    if seconds < 60:
        return 'just now'
    elif seconds < 3600:
        minutes = int(seconds / 60)
        return f'{minutes} minute{"s" if minutes > 1 else ""} ago'
    elif seconds < 86400:
        hours = int(seconds / 3600)
        return f'{hours} hour{"s" if hours > 1 else ""} ago'
    elif seconds < 604800:
        days = int(seconds / 86400)
        return f'{days} day{"s" if days > 1 else ""} ago'
    else:
        weeks = int(seconds / 604800)
        return f'{weeks} week{"s" if weeks > 1 else ""} ago'


def paginate_query(query, page=1, per_page=20):
    """Paginate a query."""
    return query.paginate(page=page, per_page=per_page, error_out=False)
