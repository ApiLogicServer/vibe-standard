from flask import Blueprint, jsonify, request
from src.services.data_service import DataService

bp = Blueprint('api', __name__)

@bp.route('/customers')
def api_customers():
    """API endpoint for customers data"""
    data_service = DataService()
    customers = data_service.get_customers()
    return jsonify([customer.to_dict() for customer in customers])

@bp.route('/customers/<customer_id>')
def api_customer_detail(customer_id):
    """API endpoint for specific customer"""
    data_service = DataService()
    customer = data_service.get_customer_by_id(customer_id)
    if customer:
        return jsonify(customer.to_dict())
    return jsonify({'error': 'Customer not found'}), 404

@bp.route('/products')
def api_products():
    """API endpoint for products data"""
    data_service = DataService()
    products = data_service.get_products()
    return jsonify([product.to_dict() for product in products])

@bp.route('/orders')
def api_orders():
    """API endpoint for orders data"""
    data_service = DataService()
    limit = request.args.get('limit', 100, type=int)
    orders = data_service.get_orders(limit=limit)
    return jsonify([order.to_dict() for order in orders])

@bp.route('/analytics/sales-by-month')
def api_sales_by_month():
    """API endpoint for monthly sales data"""
    data_service = DataService()
    sales_data = data_service.get_sales_by_month()
    return jsonify(sales_data)

@bp.route('/analytics/top-products')
def api_top_products():
    """API endpoint for top-selling products"""
    data_service = DataService()
    limit = request.args.get('limit', 10, type=int)
    top_products = data_service.get_top_products(limit=limit)
    return jsonify(top_products)

@bp.route('/analytics/sales-by-category')
def api_sales_by_category():
    """API endpoint for sales by category"""
    data_service = DataService()
    sales_data = data_service.get_sales_by_category()
    return jsonify(sales_data)

@bp.route('/analytics/customer-orders/<customer_id>')
def api_customer_orders(customer_id):
    """API endpoint for customer order history"""
    data_service = DataService()
    orders = data_service.get_customer_orders(customer_id)
    return jsonify([order.to_dict() for order in orders])

# Credit checking endpoints
@bp.route('/customers/<customer_id>/credit')
def api_customer_credit(customer_id):
    """API endpoint for customer credit check"""
    data_service = DataService()
    credit_status = data_service.check_customer_credit(customer_id)
    return jsonify(credit_status)

@bp.route('/customers/<customer_id>/credit/summary')
def api_customer_credit_summary(customer_id):
    """API endpoint for detailed customer credit summary"""
    data_service = DataService()
    credit_summary = data_service.get_customer_credit_summary(customer_id)
    return jsonify(credit_summary)

@bp.route('/orders/<int:order_id>/recalculate', methods=['POST'])
def api_recalculate_order_total(order_id):
    """API endpoint to recalculate order total"""
    data_service = DataService()
    result = data_service.update_order_totals(order_id)
    return jsonify(result)

@bp.route('/orders/recalculate-all', methods=['POST'])
def api_recalculate_all_orders():
    """API endpoint to recalculate all order totals"""
    data_service = DataService()
    result = data_service.update_order_totals()
    return jsonify(result)
