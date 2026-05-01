from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id         = db.Column(db.Integer, primary_key=True)
    name       = db.Column(db.String(100), nullable=False)
    email      = db.Column(db.String(120), unique=True, nullable=False)
    password   = db.Column(db.String(255), nullable=False)
    role       = db.Column(db.String(10), default='customer')  # 'customer' or 'admin'
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    cart_items = db.relationship('Cart', backref='user', lazy=True, cascade='all, delete-orphan')
    orders     = db.relationship('Order', backref='user', lazy=True)

    def to_dict(self):
        return {
            'id':         self.id,
            'name':       self.name,
            'email':      self.email,
            'role':       self.role,
            'created_at': self.created_at.isoformat()
        }


class Product(db.Model):
    __tablename__ = 'products'
    id          = db.Column(db.Integer, primary_key=True)
    name        = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    price       = db.Column(db.Float, nullable=False)
    image       = db.Column(db.String(500), default='')
    category    = db.Column(db.String(100), nullable=False)
    stock       = db.Column(db.Integer, default=0)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id':          self.id,
            'name':        self.name,
            'description': self.description,
            'price':       self.price,
            'image':       self.image,
            'category':    self.category,
            'stock':       self.stock,
            'created_at':  self.created_at.isoformat()
        }


class Cart(db.Model):
    __tablename__ = 'cart'
    id         = db.Column(db.Integer, primary_key=True)
    user_id    = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity   = db.Column(db.Integer, default=1)

    product = db.relationship('Product')

    def to_dict(self):
        return {
            'id':       self.id,
            'user_id':  self.user_id,
            'product':  self.product.to_dict(),
            'quantity': self.quantity
        }


class Order(db.Model):
    __tablename__ = 'orders'
    id          = db.Column(db.Integer, primary_key=True)
    user_id     = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    total_price = db.Column(db.Float, nullable=False)
    status      = db.Column(db.String(50), default='pending')  # pending, processing, shipped, delivered, cancelled
    address     = db.Column(db.Text, nullable=False)
    created_at  = db.Column(db.DateTime, default=datetime.utcnow)

    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id':          self.id,
            'user_id':     self.user_id,
            'total_price': self.total_price,
            'status':      self.status,
            'address':     self.address,
            'created_at':  self.created_at.isoformat(),
            'items':       [item.to_dict() for item in self.items]
        }


class OrderItem(db.Model):
    __tablename__ = 'order_items'
    id         = db.Column(db.Integer, primary_key=True)
    order_id   = db.Column(db.Integer, db.ForeignKey('orders.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity   = db.Column(db.Integer, nullable=False)
    price      = db.Column(db.Float, nullable=False)  # price at time of purchase

    product = db.relationship('Product')

    def to_dict(self):
        return {
            'id':         self.id,
            'order_id':   self.order_id,
            'product':    self.product.to_dict(),
            'quantity':   self.quantity,
            'price':      self.price
        }
