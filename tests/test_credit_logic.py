"""
Test script for credit business logic
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.services.credit_service import CreditService
from decimal import Decimal

def test_credit_logic():
    """Test the credit checking business logic"""
    
    # Create database connection
    db_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'nw.sqlite')
    engine = create_engine(f'sqlite:///{db_path}')
    Session = sessionmaker(bind=engine)
    session = Session()
    
    credit_service = CreditService(session)
    
    print("Testing Credit Business Logic")
    print("=" * 50)
    
    # Test customer credit check
    customer_id = "ALFKI"
    print(f"\n1. Testing credit check for customer {customer_id}")
    
    credit_status = credit_service.check_credit_limit(customer_id)
    print(f"Credit Status: {credit_status}")
    
    # Test order amount calculation
    print(f"\n2. Testing order amount calculation")
    orders = session.query(Order).filter(Order.CustomerId == customer_id).first()
    if orders:
        order_total = credit_service.calculate_order_amount_total(orders.Id)
        print(f"Order {orders.Id} calculated total: ${order_total}")
    
    # Test balance calculation
    print(f"\n3. Testing balance calculation")
    balance = credit_service.calculate_customer_balance(customer_id)
    print(f"Customer {customer_id} current balance: ${balance}")
    
    # Test item amount calculation
    print(f"\n4. Testing item amount calculation")
    test_quantity = 5
    test_price = Decimal('25.50')
    item_amount = credit_service.calculate_item_amount(test_quantity, test_price)
    print(f"Item amount for {test_quantity} units at ${test_price} each: ${item_amount}")
    
    session.close()
    print("\nCredit logic tests completed!")

if __name__ == "__main__":
    # Import the Order model
    from src.models.northwind import Order
    test_credit_logic()
