from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from src.models.northwind import *
from src.services.credit_service import CreditService
from typing import List, Dict, Any
import os

class DataService:
    """Service class for data operations on Northwind database"""
    
    def __init__(self):
        # Create database connection
        db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), 'data', 'nw.sqlite')
        engine = create_engine(f'sqlite:///{db_path}')
        Session = sessionmaker(bind=engine)
        self.session = Session()
        self.credit_service = CreditService(self.session)
    
    def __del__(self):
        if hasattr(self, 'session'):
            self.session.close()
    
    # Customer operations
    def get_customers(self) -> List[Customer]:
        """Get all customers"""
        return self.session.query(Customer).all()
    
    def get_customer_by_id(self, customer_id: str) -> Customer:
        """Get customer by ID"""
        return self.session.query(Customer).filter(Customer.Id == customer_id).first()
    
    def get_customer_count(self) -> int:
        """Get total number of customers"""
        return self.session.query(Customer).count()
    
    def get_customer_orders(self, customer_id: str) -> List[Order]:
        """Get orders for a specific customer"""
        return self.session.query(Order).filter(Order.CustomerId == customer_id).all()
    
    # Product operations
    def get_products(self) -> List[Product]:
        """Get all products"""
        return self.session.query(Product).all()
    
    def get_products_with_details(self) -> List[Dict]:
        """Get products with category and supplier details"""
        products = self.session.query(Product, Category, Supplier)\
            .join(Category, Product.CategoryId == Category.Id)\
            .join(Supplier, Product.SupplierId == Supplier.Id)\
            .all()
        
        result = []
        for product, category, supplier in products:
            product_dict = product.to_dict()
            product_dict['CategoryName'] = category.CategoryName_ColumnName
            product_dict['SupplierName'] = supplier.CompanyName
            result.append(product_dict)
        
        return result
    
    def get_product_count(self) -> int:
        """Get total number of products"""
        return self.session.query(Product).count()
    
    def get_categories(self) -> List[Category]:
        """Get all categories"""
        return self.session.query(Category).all()
    
    # Order operations
    def get_orders(self, limit: int = 100) -> List[Order]:
        """Get recent orders"""
        return self.session.query(Order)\
            .filter(Order.OrderDate.isnot(None))\
            .order_by(Order.OrderDate.desc())\
            .limit(limit)\
            .all()
    
    def get_recent_orders(self, limit: int = 50) -> List[Dict]:
        """Get recent orders with customer details"""
        orders = self.session.query(Order, Customer)\
            .join(Customer, Order.CustomerId == Customer.Id)\
            .filter(Order.OrderDate.isnot(None))\
            .order_by(Order.OrderDate.desc())\
            .limit(limit)\
            .all()
        
        result = []
        for order, customer in orders:
            order_dict = order.to_dict()
            order_dict['CustomerName'] = customer.CompanyName
            result.append(order_dict)
        
        return result
    
    def get_order_count(self) -> int:
        """Get total number of orders"""
        return self.session.query(Order).count()
    
    # Analytics operations
    def get_total_revenue(self) -> float:
        """Calculate total revenue from all orders"""
        result = self.session.query(
            func.sum(OrderDetail.Amount)
        ).scalar()
        return float(result) if result else 0.0
    
    def get_sales_by_month(self) -> List[Dict]:
        """Get sales data grouped by month"""
        results = self.session.query(
            func.strftime('%Y-%m', Order.OrderDate).label('month'),
            func.sum(OrderDetail.Amount).label('revenue')
        ).join(OrderDetail, Order.Id == OrderDetail.OrderId)\
         .filter(Order.OrderDate.isnot(None))\
         .group_by(func.strftime('%Y-%m', Order.OrderDate))\
         .order_by('month')\
         .all()
        
        return [{'month': month, 'revenue': float(revenue) if revenue else 0} for month, revenue in results if month]
    
    def get_top_products(self, limit: int = 10) -> List[Dict]:
        """Get top-selling products by revenue"""
        results = self.session.query(
            Product.ProductName,
            func.sum(OrderDetail.Amount).label('revenue'),
            func.sum(OrderDetail.Quantity).label('quantity_sold')
        ).join(OrderDetail, Product.Id == OrderDetail.ProductId)\
         .group_by(Product.Id, Product.ProductName)\
         .order_by(func.sum(OrderDetail.Amount).desc())\
         .limit(limit)\
         .all()
        
        return [
            {
                'product_name': name, 
                'revenue': float(revenue) if revenue else 0, 
                'quantity_sold': int(quantity) if quantity else 0
            } 
            for name, revenue, quantity in results
        ]
    
    def get_sales_by_category(self) -> List[Dict]:
        """Get sales data grouped by category"""
        results = self.session.query(
            Category.CategoryName_ColumnName,
            func.sum(OrderDetail.Amount).label('revenue')
        ).join(Product, Category.Id == Product.CategoryId)\
         .join(OrderDetail, Product.Id == OrderDetail.ProductId)\
         .group_by(Category.Id, Category.CategoryName_ColumnName)\
         .order_by(func.sum(OrderDetail.Amount).desc())\
         .all()
        
        return [
            {'category_name': name, 'revenue': float(revenue) if revenue else 0} 
            for name, revenue in results
        ]
    
    def get_employee_sales(self) -> List[Dict]:
        """Get sales performance by employee"""
        results = self.session.query(
            Employee.FirstName,
            Employee.LastName,
            func.count(Order.Id).label('order_count'),
            func.sum(OrderDetail.Amount).label('revenue')
        ).join(Order, Employee.Id == Order.EmployeeId)\
         .join(OrderDetail, Order.Id == OrderDetail.OrderId)\
         .group_by(Employee.Id, Employee.FirstName, Employee.LastName)\
         .order_by(func.sum(OrderDetail.Amount).desc())\
         .all()
        
        return [
            {
                'employee_name': f"{first_name} {last_name}",
                'order_count': int(order_count),
                'revenue': float(revenue) if revenue else 0
            }
            for first_name, last_name, order_count, revenue in results
        ]
    
    # Credit-related operations
    def check_customer_credit(self, customer_id: str) -> Dict[str, Any]:
        """Check customer credit status"""
        return self.credit_service.check_credit_limit(customer_id)
    
    def get_customer_credit_summary(self, customer_id: str) -> Dict[str, Any]:
        """Get comprehensive customer credit status"""
        return self.credit_service.get_credit_status_summary(customer_id)
    
    def update_order_totals(self, order_id: int = None) -> Dict[str, Any]:
        """Update order amount totals"""
        return self.credit_service.update_order_amounts(order_id)
