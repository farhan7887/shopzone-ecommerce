from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Order, OrderItem, Cart, Product, User

orders_bp = Blueprint('orders', __name__)


def is_admin(user_id):
    user = User.query.get(user_id)
    return user and user.role == 'admin'


@orders_bp.route('/', methods=['GET'])
@jwt_required()
def get_orders():
    user_id = int(get_jwt_identity())
    if is_admin(user_id):
        orders = Order.query.order_by(Order.created_at.desc()).all()
    else:
        orders = Order.query.filter_by(user_id=user_id).order_by(Order.created_at.desc()).all()
    return jsonify([o.to_dict() for o in orders]), 200


@orders_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    user_id = int(get_jwt_identity())
    order   = Order.query.get_or_404(order_id)
    if order.user_id != user_id and not is_admin(user_id):
        return jsonify({'error': 'Unauthorized'}), 403
    return jsonify(order.to_dict()), 200


@orders_bp.route('/', methods=['POST'])
@jwt_required()
def place_order():
    user_id = int(get_jwt_identity())
    data    = request.get_json()
    address = data.get('address', '').strip()

    if not address:
        return jsonify({'error': 'Shipping address is required'}), 400

    cart_items = Cart.query.filter_by(user_id=user_id).all()
    if not cart_items:
        return jsonify({'error': 'Cart is empty'}), 400

    # Check stock for all items
    for item in cart_items:
        if item.product.stock < item.quantity:
            return jsonify({'error': f'Insufficient stock for {item.product.name}'}), 400

    # Calculate total
    total = sum(item.product.price * item.quantity for item in cart_items)

    # Create order
    order = Order(user_id=user_id, total_price=total, address=address)
    db.session.add(order)
    db.session.flush()  # get order.id before commit

    # Create order items & reduce stock
    for item in cart_items:
        order_item = OrderItem(
            order_id   = order.id,
            product_id = item.product_id,
            quantity   = item.quantity,
            price      = item.product.price
        )
        item.product.stock -= item.quantity
        db.session.add(order_item)

    # Clear cart
    Cart.query.filter_by(user_id=user_id).delete()
    db.session.commit()

    return jsonify(order.to_dict()), 201


@orders_bp.route('/<int:order_id>/status', methods=['PUT'])
@jwt_required()
def update_order_status(order_id):
    user_id = int(get_jwt_identity())
    if not is_admin(user_id):
        return jsonify({'error': 'Admin access required'}), 403

    order  = Order.query.get_or_404(order_id)
    data   = request.get_json()
    status = data.get('status')

    valid_statuses = ['pending', 'processing', 'shipped', 'delivered', 'cancelled']
    if status not in valid_statuses:
        return jsonify({'error': 'Invalid status'}), 400

    order.status = status
    db.session.commit()
    return jsonify(order.to_dict()), 200


@orders_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_stats():
    user_id = int(get_jwt_identity())
    if not is_admin(user_id):
        return jsonify({'error': 'Admin access required'}), 403

    total_orders   = Order.query.count()
    total_revenue  = db.session.query(db.func.sum(Order.total_price)).scalar() or 0
    total_products = Product.query.count()
    total_users    = User.query.filter_by(role='customer').count()
    pending_orders = Order.query.filter_by(status='pending').count()

    return jsonify({
        'total_orders':   total_orders,
        'total_revenue':  round(total_revenue, 2),
        'total_products': total_products,
        'total_users':    total_users,
        'pending_orders': pending_orders
    }), 200
