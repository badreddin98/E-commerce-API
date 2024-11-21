from flask import Blueprint, request, jsonify
from extensions import db
from models import Product

bp = Blueprint('product', __name__, url_prefix='/api')

@bp.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()
    
    try:
        product = Product(
            name=data['name'],
            price=data['price'],
            stock=data.get('stock', 0),
            restock_threshold=data.get('restock_threshold', 10)
        )
        db.session.add(product)
        db.session.commit()
        return jsonify({'message': 'Product created successfully', 'id': product.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/products', methods=['GET'])
def list_products():
    products = Product.query.all()
    return jsonify([{
        'id': p.id,
        'name': p.name,
        'price': p.price,
        'stock': p.stock,
        'restock_threshold': p.restock_threshold
    } for p in products])

@bp.route('/products/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify({
        'id': product.id,
        'name': product.name,
        'price': product.price,
        'stock': product.stock,
        'restock_threshold': product.restock_threshold
    })

@bp.route('/products/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    
    try:
        if 'name' in data:
            product.name = data['name']
        if 'price' in data:
            product.price = data['price']
        if 'stock' in data:
            product.stock = data['stock']
        if 'restock_threshold' in data:
            product.restock_threshold = data['restock_threshold']
            
        db.session.commit()
        return jsonify({'message': 'Product updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/products/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({'message': 'Product deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/products/<int:id>/stock', methods=['GET'])
def get_stock_level(id):
    product = Product.query.get_or_404(id)
    needs_restock = product.stock <= product.restock_threshold
    return jsonify({
        'product_id': product.id,
        'stock_level': product.stock,
        'restock_threshold': product.restock_threshold,
        'needs_restock': needs_restock
    })

@bp.route('/products/<int:id>/restock', methods=['POST'])
def restock_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    
    try:
        quantity = data.get('quantity', 0)
        if quantity > 0:
            product.stock += quantity
            db.session.commit()
            return jsonify({
                'message': f'Added {quantity} items to stock',
                'new_stock_level': product.stock
            })
        return jsonify({'error': 'Quantity must be greater than 0'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
