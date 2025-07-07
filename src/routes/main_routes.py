from flask import Blueprint, render_template
from src.services.data_service import DataService

bp = Blueprint('main', __name__)

@bp.route('/dashboard')
def dashboard():
    """Main dashboard with key metrics"""
    try:
        data_service = DataService()
        
        # Get summary statistics
        stats = {
            'total_customers': data_service.get_customer_count(),
            'total_orders': data_service.get_order_count(),
            'total_products': data_service.get_product_count(),
            'total_revenue': data_service.get_total_revenue()
        }
        
        return render_template('dashboard.html', stats=stats)
    except Exception as e:
        # If there's an error, show dashboard with empty stats
        stats = {
            'total_customers': 0,
            'total_orders': 0,
            'total_products': 0,
            'total_revenue': 0.0
        }
        return render_template('dashboard.html', stats=stats)

@bp.route('/customers')
def customers():
    """Customer list and analysis"""
    try:
        data_service = DataService()
        customers = data_service.get_customers()
        
        # Process customers for template
        customers_list = [customer.to_dict() for customer in customers]
        
        # Group by country for display
        countries = {}
        for customer in customers_list:
            country = customer.get('Country') or 'Unknown'
            if country not in countries:
                countries[country] = 0
            countries[country] += 1
        
        return render_template('customers.html', customers=customers_list, countries=countries)
    except Exception as e:
        print(f"Error in customers route: {e}")  # Debug print
        return render_template('customers.html', customers=[], countries={})

@bp.route('/customers/<customer_id>')
def customer_detail(customer_id):
    """Customer detail page with orders"""
    try:
        data_service = DataService()
        customer = data_service.get_customer_by_id(customer_id)
        
        if not customer:
            return render_template('404.html'), 404
            
        orders = data_service.get_customer_orders(customer_id)
        
        # Calculate customer statistics
        total_orders = len(orders)
        total_spent = sum(float(order.AmountTotal or 0) for order in orders)
        
        # Get credit information
        credit_status = data_service.check_customer_credit(customer_id)
        
        return render_template('customer_detail.html', 
                             customer=customer, 
                             orders=orders,
                             total_orders=total_orders,
                             total_spent=total_spent,
                             credit_status=credit_status)
    except Exception as e:
        print(f"Error in customer detail route: {e}")
        return render_template('404.html'), 404

@bp.route('/products')
def products():
    """Product catalog and analysis"""
    try:
        data_service = DataService()
        products = data_service.get_products_with_details()
        categories = data_service.get_categories()
        return render_template('products.html', products=products, categories=categories)
    except Exception as e:
        return render_template('products.html', products=[], categories=[])

@bp.route('/orders')
def orders():
    """Order history and analysis"""
    try:
        data_service = DataService()
        orders = data_service.get_recent_orders()
        
        # Process orders for template
        orders_list = [order for order in orders]
        
        # Group by country for display
        countries = {}
        for order in orders_list:
            country = order.get('ShipCountry') or 'Unknown'
            if country not in countries:
                countries[country] = 0
            countries[country] += 1
        
        return render_template('orders.html', orders=orders_list, countries=countries)
    except Exception as e:
        print(f"Error in orders route: {e}")  # Debug print
        return render_template('orders.html', orders=[], countries={})

@bp.route('/analytics')
def analytics():
    """Advanced analytics and charts"""
    try:
        data_service = DataService()
        
        # Get data for various charts
        sales_by_month = data_service.get_sales_by_month()
        top_products = data_service.get_top_products()
        sales_by_category = data_service.get_sales_by_category()
        
        return render_template('analytics.html', 
                             sales_by_month=sales_by_month,
                             top_products=top_products,
                             sales_by_category=sales_by_category)
    except Exception as e:
        return render_template('analytics.html', 
                             sales_by_month=[],
                             top_products=[],
                             sales_by_category=[])

@bp.route('/credit')
def credit_management():
    """Credit management page"""
    try:
        data_service = DataService()
        
        # Get customers with credit limits
        customers = data_service.get_customers()
        customers_with_credit = []
        
        for customer in customers:
            if customer.CreditLimit and customer.CreditLimit > 0:
                credit_check = data_service.check_customer_credit(customer.Id)
                if credit_check['success']:
                    customers_with_credit.append(credit_check)
        
        # Sort by balance percentage (highest risk first)
        customers_with_credit.sort(key=lambda x: x['balance_percentage'], reverse=True)
        
        return render_template('credit_management.html', customers=customers_with_credit)
    except Exception as e:
        print(f"Error in credit management route: {e}")
        return render_template('credit_management.html', customers=[])
