from flask import Flask
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from models import db, User, Product
import bcrypt
import os

app = Flask(__name__)

# ── Config ──────────────────────────────────────────────────────────────────
app.config['SQLALCHEMY_DATABASE_URI']        = 'sqlite:///ecommerce.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY']                 = 'shopify-clone-super-secret-key-2026'

# ── Extensions ───────────────────────────────────────────────────────────────
db.init_app(app)
JWTManager(app)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ── Blueprints ───────────────────────────────────────────────────────────────
from routes.auth     import auth_bp
from routes.products import products_bp
from routes.cart     import cart_bp
from routes.orders   import orders_bp

app.register_blueprint(auth_bp,     url_prefix='/api/auth')
app.register_blueprint(products_bp, url_prefix='/api/products')
app.register_blueprint(cart_bp,     url_prefix='/api/cart')
app.register_blueprint(orders_bp,   url_prefix='/api/orders')


# ── Seed Data ────────────────────────────────────────────────────────────────
def seed_data():
    # Admin user
    if not User.query.filter_by(email='admin@shop.com').first():
        hashed = bcrypt.hashpw(b'admin123', bcrypt.gensalt())
        admin  = User(name='Admin', email='admin@shop.com',
                      password=hashed.decode('utf-8'), role='admin')
        db.session.add(admin)

    # Demo customer
    if not User.query.filter_by(email='user@shop.com').first():
        hashed = bcrypt.hashpw(b'user123', bcrypt.gensalt())
        user   = User(name='Ali Hassan', email='user@shop.com',
                      password=hashed.decode('utf-8'), role='customer')
        db.session.add(user)

    # Sample products
    if Product.query.count() == 0:
        products = [
            Product(name='iPhone 15 Pro', description='Latest Apple flagship with titanium design, A17 Pro chip, and pro camera system.', price=299999, image='https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=400', category='Electronics', stock=25),
            Product(name='Samsung Galaxy S24', description='Android powerhouse with AI features, Snapdragon 8 Gen 3, and brilliant display.', price=229999, image='https://images.unsplash.com/photo-1707757292019-55e45ba97a5e?w=400', category='Electronics', stock=30),
            Product(name='Sony WH-1000XM5', description='Industry-leading noise cancelling headphones with 30-hour battery life.', price=79999, image='https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=400', category='Electronics', stock=50),
            Product(name='MacBook Air M3', description='Incredibly thin laptop with M3 chip, 18-hour battery, and stunning Liquid Retina display.', price=349999, image='https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=400', category='Electronics', stock=15),
            Product(name='Nike Air Max 270', description='Iconic Nike silhouette with large Air unit for all-day comfort and bold style.', price=24999, image='https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=400', category='Footwear', stock=60),
            Product(name='Adidas Ultraboost 23', description='Premium running shoes with responsive Boost cushioning and Primeknit upper.', price=22999, image='https://images.unsplash.com/photo-1608231387042-66d1773070a5?w=400', category='Footwear', stock=45),
            Product(name='Levi\'s 501 Jeans', description='The original blue jean. Straight fit with button fly, made from premium denim.', price=8999, image='https://images.unsplash.com/photo-1542272604-787c3835535d?w=400', category='Clothing', stock=100),
            Product(name='The North Face Jacket', description='Waterproof and windproof jacket with DryVent technology for all-weather adventures.', price=34999, image='https://images.unsplash.com/photo-1591047139829-d91aecb6caea?w=400', category='Clothing', stock=35),
            Product(name='Dyson V15 Vacuum', description='Laser-powered cordless vacuum with intelligent auto-sensing suction and HEPA filtration.', price=129999, image='https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=400', category='Home', stock=20),
            Product(name='Instant Pot Duo', description='7-in-1 electric pressure cooker that replaces 7 kitchen appliances. 6-quart capacity.', price=19999, image='https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=400', category='Home', stock=40),
            Product(name='Harry Potter Box Set', description='Complete 7-book hardcover collection of the wizarding world saga by J.K. Rowling.', price=12999, image='https://images.unsplash.com/photo-1551029506-0807df4e2031?w=400', category='Books', stock=80),
            Product(name='Atomic Habits', description='Proven framework for building good habits and breaking bad ones by James Clear.', price=2999, image='https://images.unsplash.com/photo-1544947950-fa07a98d237f?w=400', category='Books', stock=120),
        ]
        for p in products:
            db.session.add(p)

    db.session.commit()
    print("✅ Database seeded successfully!")


# ── Init DB ──────────────────────────────────────────────────────────────────
with app.app_context():
    db.create_all()
    seed_data()

if __name__ == '__main__':
    print("\n🚀 ShopZone Backend running at http://localhost:5000")
    print("👤 Admin login  → admin@shop.com  / admin123")
    print("👤 User login   → user@shop.com   / user123\n")
    app.run(debug=True, port=5000)
