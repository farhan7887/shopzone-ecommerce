from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Product, User

products_bp = Blueprint('products', __name__)


def is_admin(user_id):
    user = User.query.get(user_id)
    return user and user.role == 'admin'


@products_bp.route('/', methods=['GET'])
def get_products():
    category = request.args.get('category')
    search   = request.args.get('search')
    query    = Product.query

    if category:
        query = query.filter_by(category=category)
    if search:
        query = query.filter(Product.name.ilike(f'%{search}%'))

    products = query.order_by(Product.created_at.desc()).all()
    return jsonify([p.to_dict() for p in products]), 200


@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = Product.query.get_or_404(product_id)
    return jsonify(product.to_dict()), 200


@products_bp.route('/categories', methods=['GET'])
def get_categories():
    rows = db.session.query(Product.category).distinct().all()
    return jsonify([r[0] for r in rows]), 200


@products_bp.route('/', methods=['POST'])
@jwt_required()
def create_product():
    user_id = int(get_jwt_identity())
    if not is_admin(user_id):
        return jsonify({'error': 'Admin access required'}), 403

    data = request.get_json()
    product = Product(
        name        = data['name'],
        description = data['description'],
        price       = float(data['price']),
        image       = data.get('image', ''),
        category    = data['category'],
        stock       = int(data.get('stock', 0))
    )
    db.session.add(product)
    db.session.commit()
    return jsonify(product.to_dict()), 201


@products_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    user_id = int(get_jwt_identity())
    if not is_admin(user_id):
        return jsonify({'error': 'Admin access required'}), 403

    product = Product.query.get_or_404(product_id)
    data    = request.get_json()

    product.name        = data.get('name',        product.name)
    product.description = data.get('description', product.description)
    product.price       = float(data.get('price', product.price))
    product.image       = data.get('image',       product.image)
    product.category    = data.get('category',    product.category)
    product.stock       = int(data.get('stock',   product.stock))

    db.session.commit()
    return jsonify(product.to_dict()), 200


@products_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    user_id = int(get_jwt_identity())
    if not is_admin(user_id):
        return jsonify({'error': 'Admin access required'}), 403

    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    return jsonify({'message': 'Product deleted'}), 200
