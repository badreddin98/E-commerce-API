from flask import Blueprint, request, jsonify
from extensions import db
from models import Order, OrderItem, Product
from datetime import datetime

bp = Blueprint('order', __name__, url_prefix='/api')

@bp.route('/orders', methods=['POST'])
def create_order():
    data = request.get_json()
    
    try:
        # Calculate total price and check stock
        total_price = 0
        order_items = []
        
        for item in data['items']:
            product = Product.query.get_or_404(item['product_id'])
            if product.stock < item['quantity']:
                return jsonify({'error': f'Insufficient stock for product {product.name}'}), 400
                
            total_price += product.price * item['quantity']
            order_items.append({
                'product': product,
                'quantity': item['quantity'],
                'price_at_time': product.price
            })
        
        # Create order
        order = Order(
            customer_id=data['customer_id'],
            total_price=total_price,
            status='pending'
        )
        db.session.add(order)
        
        # Create order items and update stock
        for item in order_items:
            order_item = OrderItem(
                order=order,
                product=item['product'],
                quantity=item['quantity'],
                price_at_time=item['price_at_time']
            )
            db.session.add(order_item)
            
            # Update stock
            item['product'].stock -= item['quantity']
        
        db.session.commit()
        return jsonify({
            'message': 'Order created successfully',
            'order_id': order.id,
            'total_price': total_price
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/orders/<int:id>', methods=['GET'])
def get_order(id):
    order = Order.query.get_or_404(id)
    return jsonify({
        'id': order.id,
        'customer_id': order.customer_id,
        'status': order.status,
        'order_date': order.order_date,
        'total_price': order.total_price,
        'items': [{
            'product_id': item.product_id,
            'quantity': item.quantity,
            'price_at_time': item.price_at_time
        } for item in order.items]
    })

@bp.route('/orders', methods=['GET'])
def get_customer_orders():
    customer_id = request.args.get('customer_id', type=int)
    if not customer_id:
        return jsonify({'error': 'customer_id parameter is required'}), 400
        
    orders = Order.query.filter_by(customer_id=customer_id).all()
    return jsonify([{
        'id': order.id,
        'status': order.status,
        'order_date': order.order_date,
        'total_price': order.total_price
    } for order in orders])

@bp.route('/orders/<int:id>/cancel', methods=['PUT'])
def cancel_order(id):
    order = Order.query.get_or_404(id)
    
    if order.status != 'pending':
        return jsonify({'error': 'Only pending orders can be cancelled'}), 400
        
    try:
        # Return items to stock
        for item in order.items:
            item.product.stock += item.quantity
            
        order.status = 'cancelled'
        db.session.commit()
        return jsonify({'message': 'Order cancelled successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/orders/<int:id>/total', methods=['GET'])
def get_order_total(id):
    order = Order.query.get_or_404(id)
    return jsonify({
        'order_id': order.id,
        'total_price': order.total_price,
        'items_count': len(order.items)
    })
