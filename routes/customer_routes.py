from flask import Blueprint, request, jsonify
from extensions import db
from models import Customer, CustomerAccount

bp = Blueprint('customer', __name__, url_prefix='/api')

@bp.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    
    try:
        customer = Customer(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone', '')
        )
        db.session.add(customer)
        db.session.commit()
        return jsonify({'message': 'Customer created successfully', 'id': customer.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/customers/<int:id>', methods=['GET'])
def get_customer(id):
    customer = Customer.query.get_or_404(id)
    return jsonify({
        'id': customer.id,
        'name': customer.name,
        'email': customer.email,
        'phone': customer.phone
    })

@bp.route('/customers/<int:id>', methods=['PUT'])
def update_customer(id):
    customer = Customer.query.get_or_404(id)
    data = request.get_json()
    
    try:
        if 'name' in data:
            customer.name = data['name']
        if 'email' in data:
            customer.email = data['email']
        if 'phone' in data:
            customer.phone = data['phone']
            
        db.session.commit()
        return jsonify({'message': 'Customer updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/customers/<int:id>', methods=['DELETE'])
def delete_customer(id):
    customer = Customer.query.get_or_404(id)
    try:
        db.session.delete(customer)
        db.session.commit()
        return jsonify({'message': 'Customer deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/customer-accounts', methods=['POST'])
def create_customer_account():
    data = request.get_json()
    
    try:
        account = CustomerAccount(
            username=data['username'],
            customer_id=data['customer_id']
        )
        account.set_password(data['password'])
        
        db.session.add(account)
        db.session.commit()
        return jsonify({'message': 'Customer account created successfully', 'id': account.id}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/customer-accounts/<int:id>', methods=['GET'])
def get_customer_account(id):
    account = CustomerAccount.query.get_or_404(id)
    return jsonify({
        'id': account.id,
        'username': account.username,
        'customer_id': account.customer_id
    })

@bp.route('/customer-accounts/<int:id>', methods=['PUT'])
def update_customer_account(id):
    account = CustomerAccount.query.get_or_404(id)
    data = request.get_json()
    
    try:
        if 'username' in data:
            account.username = data['username']
        if 'password' in data:
            account.set_password(data['password'])
            
        db.session.commit()
        return jsonify({'message': 'Customer account updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400

@bp.route('/customer-accounts/<int:id>', methods=['DELETE'])
def delete_customer_account(id):
    account = CustomerAccount.query.get_or_404(id)
    try:
        db.session.delete(account)
        db.session.commit()
        return jsonify({'message': 'Customer account deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 400
