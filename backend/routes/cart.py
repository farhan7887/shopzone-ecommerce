from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Cart, Product

cart_bp = Blueprint('cart', __name__)


@cart_bp.route('/', methods=['GET'])
@jwt_required()
def get_cart():
    user_id = int(get_jwt_identity())
    items   = Cart.query.filter_by(user_id=user_id).all()
    return jsonify([i.to_dict() for i in items]), 200


@cart_bp.route('/', methods=['POST'])
@jwt_required()
def add_to_cart():
    user_id    = int(get_jwt_identity())
    data       = request.get_json()
    product_id = int(data.get('product_id'))
    quantity   = int(data.get('quantity', 1))

    product = Product.query.get_or_404(product_id)
    if product.stock < quantity:
        return jsonify({'error': 'Insufficient stock'}), 400

    existing = Cart.query.filter_by(user_id=user_id, product_id=product_id).first()
    if existing:
        existing.quantity += quantity
    else:
        item = Cart(user_id=user_id, product_id=product_id, quantity=quantity)
        db.session.add(item)

    db.session.commit()
    return jsonify({'message': 'Added to cart'}), 200


@cart_bp.route('/<int:item_id>', methods=['PUT'])
@jwt_required()
def update_cart_item(item_id):
    user_id  = int(get_jwt_identity())
    item     = Cart.query.filter_by(id=item_id, user_id=user_id).first_or_404()
    data     = request.get_json()
    quantity = int(data.get('quantity', 1))

    if quantity <= 0:
        db.session.delete(item)
    else:
        item.quantity = quantity

    db.session.commit()
    return jsonify({'message': 'Cart updated'}), 200


@cart_bp.route('/<int:item_id>', methods=['DELETE'])
@jwt_required()
def remove_cart_item(item_id):
    user_id = int(get_jwt_identity())
    item    = Cart.query.filter_by(id=item_id, user_id=user_id).first_or_404()
    db.session.delete(item)
    db.session.commit()
    return jsonify({'message': 'Item removed'}), 200


@cart_bp.route('/', methods=['DELETE'])
@jwt_required()
def clear_cart():
    user_id = int(get_jwt_identity())
    Cart.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    return jsonify({'message': 'Cart cleared'}), 200
