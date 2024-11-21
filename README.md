# E-commerce API Project

A comprehensive RESTful API for an e-commerce platform built with Flask and SQLAlchemy.

## Features

- Customer Management
  - Create, read, update, and delete customers
  - Manage customer accounts with secure password hashing
  - JWT-based authentication

- Product Catalog
  - Create, read, update, and delete products
  - Track product inventory
  - Manage stock levels and restock thresholds

- Order Processing
  - Place new orders
  - Track order status
  - View order history
  - Calculate order totals
  - Cancel orders

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd e-commerce-api
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up the database:
```bash
flask db upgrade
```

## API Endpoints

### Authentication
- POST /api/auth/login - Login with username and password
- POST /api/auth/register - Register a new customer account

### Customers
- POST /api/customers - Create a new customer
- GET /api/customers/{id} - Get customer details
- PUT /api/customers/{id} - Update customer information
- DELETE /api/customers/{id} - Delete a customer

### Products
- POST /api/products - Create a new product
- GET /api/products - List all products
- GET /api/products/{id} - Get product details
- PUT /api/products/{id} - Update product information
- DELETE /api/products/{id} - Delete a product
- GET /api/products/{id}/stock - Get product stock level
- PUT /api/products/{id}/restock - Restock a product

### Orders
- POST /api/orders - Place a new order
- GET /api/orders/{id} - Get order details
- GET /api/orders/customer/{id} - Get customer's order history
- PUT /api/orders/{id}/cancel - Cancel an order
- GET /api/orders/{id}/total - Calculate order total

## Authentication

The API uses JWT (JSON Web Tokens) for authentication. To access protected endpoints:

1. Register a new account or login to get a JWT token
2. Include the token in the Authorization header:
```
Authorization: Bearer <your-token>
```

## Error Handling

The API provides detailed error messages and appropriate HTTP status codes:

- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 404: Not Found
- 500: Internal Server Error

## Testing

Run the tests using:
```bash
python -m pytest
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
