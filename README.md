# CreatorHub - Digital Marketplace for Creators

[![Python](https://img.shields.io/badge/Python-3.12%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.0.0-green)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow)](LICENSE)

CreatorHub is a production-ready digital marketplace web application inspired by Buy Me a Coffee, Gumroad, and Payhip. It empowers creators to sell digital products like eBooks, PDFs, source code, templates, courses, and other downloadable content.

## 🚀 Features

### For Users
- 📝 User registration and authentication (Email, Google OAuth)
- 🔐 Email verification and password reset
- 🛒 Browse and purchase digital products
- 💳 Secure checkout with multiple payment options
- 📥 Download purchased products with expiration links
- ⭐ Rate and review products
- ❤️ Wishlist functionality
- 👥 Follow favorite creators
- 💝 Support creators with custom amounts
- 📊 Purchase history and invoices

### For Creators
- 📦 Upload and manage digital products
- 🎨 Product gallery and preview images
- 💰 Set flexible pricing and discounts
- 📊 Comprehensive analytics dashboard
- 📈 Sales and revenue tracking
- 👥 Customer management
- 🏷️ Coupon system
- 🎁 Membership programs (Monthly/Yearly)
- 👤 Profile customization
- 💬 Supporter wall and messages

### For Administrators
- 👥 User and creator management
- 📦 Product moderation
- 💳 Payment management
- 📊 Analytics and reporting
- 🔧 Website settings
- 📧 Email template management

### Security Features
- 🔐 Password hashing with bcrypt
- 🛡️ CSRF protection
- 🚫 XSS protection
- 🔒 SQL injection prevention
- ⚡ Rate limiting
- 🎯 Secure headers with Talisman
- 📝 Signed download links
- 🔑 Environment-based configuration

## 📋 Tech Stack

### Backend
- **Framework:** Flask 3.0.0
- **Database:** SQLite (Dev), PostgreSQL (Production)
- **ORM:** SQLAlchemy 2.0
- **Authentication:** Flask-Login, Flask-Bcrypt
- **Payment:** Stripe, Razorpay
- **Storage:** Local (Dev), AWS S3 (Production)
- **Email:** Flask-Mail
- **Security:** Flask-Talisman, Flask-Limiter

### Frontend
- **Markup:** HTML5
- **Styling:** Tailwind CSS
- **Scripting:** Vanilla JavaScript, Alpine.js
- **Templating:** Jinja2
- **Charts:** Chart.js
- **Icons:** Font Awesome

## 📁 Project Structure

```
creatorhub/
├── app/
│   ├── __init__.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── creator.py
│   │   ├── product.py
│   │   └── ...
│   ├── blueprints/
│   │   ├── auth/
│   │   ├── creator/
│   │   ├── products/
│   │   ├── orders/
│   │   ├── payments/
│   │   ├── downloads/
│   │   ├── dashboard/
│   │   ├── admin/
│   │   └── api/
│   ├── templates/
│   │   ├── base.html
│   │   ├── home.html
│   │   ├── auth/
│   │   ├── products/
│   │   └── ...
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   └── utils/
│       ├── decorators.py
│       ├── helpers.py
│       └── email.py
├── instance/
├── migrations/
├── config.py
├── run.py
├── requirements.txt
└── README.md
```

## 🛠️ Installation

### Prerequisites
- Python 3.12 or higher
- pip (Python package manager)
- Git

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/CreatorHub.git
cd CreatorHub
```

### Step 2: Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Configure Environment Variables

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your configuration
nano .env
```

### Step 5: Initialize Database

```bash
# Create migrations directory
flask db init

# Generate initial migration
flask db migrate -m "Initial migration"

# Apply migrations
flask db upgrade
```

### Step 6: Create Admin User

```bash
flask shell
>>> from app.models import User, Creator
>>> admin = User(email='admin@creatorhub.com', username='admin', is_admin=True)
>>> admin.set_password('your_secure_password')
>>> db.session.add(admin)
>>> db.session.commit()
>>> exit()
```

### Step 7: Run Application

```bash
python run.py
```

Access the application at `http://localhost:5000`

## 🔧 Configuration

### Email Configuration

Update your `.env` file with SMTP credentials:

```env
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
```

### Payment Gateway Setup

#### Stripe
1. Create account at https://stripe.com
2. Get API keys from Dashboard
3. Update `.env`:

```env
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

#### Razorpay
1. Create account at https://razorpay.com
2. Get API keys from Settings
3. Update `.env`:

```env
RAZORPAY_KEY_ID=rzp_test_...
RAZORPAY_KEY_SECRET=...
RAZORPAY_WEBHOOK_SECRET=...
```

### AWS S3 Configuration (Production)

```env
AWS_ACCESS_KEY_ID=your_access_key
AWS_SECRET_ACCESS_KEY=your_secret_key
AWS_S3_BUCKET=your-bucket-name
AWS_S3_REGION=us-east-1
```

## 📦 Database Models

The application includes the following models:

- **User** - Registered users and customers
- **Creator** - Creator profiles and information
- **Product** - Digital products for sale
- **Category** - Product categories
- **Order** - Customer orders
- **Payment** - Payment transactions
- **Download** - Download records and links
- **Review** - Product reviews and ratings
- **Follower** - Creator followers
- **Membership** - Membership plans and subscriptions
- **Coupon** - Discount coupons
- **Notification** - User notifications
- **Message** - Creator/customer messages
- **Support** - Support/tip transactions

## 🚀 Deployment

### Using Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:8000 run:app
```

### Using Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.12-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "run:app"]
```

Build and run:

```bash
docker build -t creatorhub .
docker run -p 8000:8000 creatorhub
```

### Deployment Platforms

- **Render** - https://render.com
- **Railway** - https://railway.app
- **PythonAnywhere** - https://pythonanywhere.com
- **DigitalOcean** - https://digitalocean.com
- **AWS EC2** - https://aws.amazon.com/ec2/
- **Heroku** - https://www.heroku.com

## 📚 API Documentation

The application provides REST API endpoints:

```
GET  /api/products              - List products
GET  /api/products/<id>         - Get product details
POST /api/orders                - Create order
GET  /api/orders/<id>           - Get order details
GET  /api/creators/<id>         - Get creator profile
POST /api/support               - Send support/tip
GET  /api/downloads/<id>        - Generate download link
```

## 🔒 Security Best Practices

1. **Environment Variables** - Keep sensitive data in `.env`
2. **HTTPS** - Use HTTPS in production
3. **CSRF Protection** - Enabled by default
4. **Rate Limiting** - Applied to critical endpoints
5. **Password Hashing** - Bcrypt with salt
6. **Signed URLs** - For download links
7. **Input Validation** - WTForms validation
8. **SQL Injection Prevention** - SQLAlchemy parameterized queries

## 🧪 Testing

Run tests:

```bash
pytest
```

With coverage:

```bash
pytest --cov=app
```

## 📊 Performance Optimization

- Image lazy loading
- Database query optimization
- Caching with Redis (production)
- Pagination for large datasets
- Asset compression
- CDN integration ready

## 🐛 Troubleshooting

### Database Issues

```bash
# Reset database
rm instance/creatorhub.db
flask db upgrade
```

### Port Already in Use

```bash
python run.py --port 5001
```

### Email Not Sending

- Verify SMTP credentials in `.env`
- Check email provider settings
- Enable "Less secure app access" for Gmail

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📧 Support

For support, email support@creatorhub.com or open an issue on GitHub.

## 🙏 Acknowledgments

- Inspired by Buy Me a Coffee, Gumroad, and Payhip
- Built with Flask and Tailwind CSS
- Payment processing with Stripe and Razorpay

---

**Made with ❤️ for Creators**
