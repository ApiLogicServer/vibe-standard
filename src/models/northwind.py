from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Customer(Base):
    """Customer model for Northwind database"""
    __tablename__ = 'Customer'
    
    Id = Column(String(8000), primary_key=True)
    CompanyName = Column(String(8000))
    ContactName = Column(String(8000))
    ContactTitle = Column(String(8000))
    Address = Column(String(8000))
    City = Column(String(8000))
    Region = Column(String(8000))
    PostalCode = Column(String(8000))
    Country = Column(String(8000))
    Phone = Column(String(8000))
    Fax = Column(String(8000))
    Balance = Column(Numeric)
    CreditLimit = Column(Numeric)
    OrderCount = Column(Integer, default=0)
    UnpaidOrderCount = Column(Integer, default=0)
    Client_id = Column(Integer)
    
    # Relationships
    orders = relationship("Order", back_populates="customer")
    
    def to_dict(self):
        return {
            'Id': self.Id,
            'CompanyName': self.CompanyName,
            'ContactName': self.ContactName,
            'ContactTitle': self.ContactTitle,
            'Address': self.Address,
            'City': self.City,
            'Region': self.Region,
            'PostalCode': self.PostalCode,
            'Country': self.Country,
            'Phone': self.Phone,
            'Fax': self.Fax,
            'Balance': float(self.Balance) if self.Balance else None,
            'CreditLimit': float(self.CreditLimit) if self.CreditLimit else None,
            'OrderCount': self.OrderCount,
            'UnpaidOrderCount': self.UnpaidOrderCount
        }

class Category(Base):
    """Category model for Northwind database"""
    __tablename__ = 'CategoryTableNameTest'
    
    Id = Column(Integer, primary_key=True)
    CategoryName_ColumnName = Column(String(8000))
    Description = Column(String(8000))
    Client_id = Column(Integer)
    
    # Relationships
    products = relationship("Product", back_populates="category")
    
    def to_dict(self):
        return {
            'Id': self.Id,
            'CategoryName': self.CategoryName_ColumnName,
            'Description': self.Description,
            'Client_id': self.Client_id
        }

class Supplier(Base):
    """Supplier model for Northwind database"""
    __tablename__ = 'Supplier'
    
    Id = Column(Integer, primary_key=True)
    CompanyName = Column(String(8000))
    ContactName = Column(String(8000))
    ContactTitle = Column(String(8000))
    Address = Column(String(8000))
    City = Column(String(8000))
    Region = Column(String(8000))
    PostalCode = Column(String(8000))
    Country = Column(String(8000))
    Phone = Column(String(8000))
    Fax = Column(String(8000))
    HomePage = Column(String(8000))
    
    # Relationships
    products = relationship("Product", back_populates="supplier")
    
    def to_dict(self):
        return {
            'Id': self.Id,
            'CompanyName': self.CompanyName,
            'ContactName': self.ContactName,
            'ContactTitle': self.ContactTitle,
            'Address': self.Address,
            'City': self.City,
            'Region': self.Region,
            'PostalCode': self.PostalCode,
            'Country': self.Country,
            'Phone': self.Phone,
            'Fax': self.Fax,
            'HomePage': self.HomePage
        }

class Product(Base):
    """Product model for Northwind database"""
    __tablename__ = 'Product'
    
    Id = Column(Integer, primary_key=True)
    ProductName = Column(String(8000))
    SupplierId = Column(Integer, ForeignKey('Supplier.Id'), nullable=False)
    CategoryId = Column(Integer, ForeignKey('CategoryTableNameTest.Id'), nullable=False)
    QuantityPerUnit = Column(String(8000))
    UnitPrice = Column(Numeric, nullable=False)
    UnitsInStock = Column(Integer, nullable=False)
    UnitsOnOrder = Column(Integer, nullable=False)
    ReorderLevel = Column(Integer, nullable=False)
    Discontinued = Column(Integer, nullable=False)
    UnitsShipped = Column(Integer)
    
    # Relationships
    supplier = relationship("Supplier", back_populates="products")
    category = relationship("Category", back_populates="products")
    order_details = relationship("OrderDetail", back_populates="product")
    
    def to_dict(self):
        return {
            'Id': self.Id,
            'ProductName': self.ProductName,
            'SupplierId': self.SupplierId,
            'CategoryId': self.CategoryId,
            'QuantityPerUnit': self.QuantityPerUnit,
            'UnitPrice': float(self.UnitPrice) if self.UnitPrice else None,
            'UnitsInStock': self.UnitsInStock,
            'UnitsOnOrder': self.UnitsOnOrder,
            'ReorderLevel': self.ReorderLevel,
            'Discontinued': self.Discontinued,
            'UnitsShipped': self.UnitsShipped
        }

class Employee(Base):
    """Employee model for Northwind database"""
    __tablename__ = 'Employee'
    
    Id = Column(Integer, primary_key=True)
    LastName = Column(String(8000))
    FirstName = Column(String(8000))
    Title = Column(String(8000))
    TitleOfCourtesy = Column(String(8000))
    BirthDate = Column(String(8000))
    HireDate = Column(String(8000))
    Address = Column(String(8000))
    City = Column(String(8000))
    Region = Column(String(8000))
    PostalCode = Column(String(8000))
    Country = Column(String(8000))
    HomePhone = Column(String(8000))
    Extension = Column(String(8000))
    Notes = Column(String(8000))
    ReportsTo = Column(Integer, ForeignKey('Employee.Id'))
    PhotoPath = Column(String(8000))
    EmployeeType = Column(String(16), default='Salaried')
    Salary = Column(Numeric)
    WorksForDepartmentId = Column(Integer)
    OnLoanDepartmentId = Column(Integer)
    UnionId = Column(Integer)
    Dues = Column(Numeric)
    Email = Column(Text)
    
    # Relationships
    manager = relationship("Employee", remote_side=[Id], back_populates="subordinates")
    subordinates = relationship("Employee", back_populates="manager")
    orders = relationship("Order", back_populates="employee")
    
    def to_dict(self):
        return {
            'Id': self.Id,
            'LastName': self.LastName,
            'FirstName': self.FirstName,
            'Title': self.Title,
            'TitleOfCourtesy': self.TitleOfCourtesy,
            'BirthDate': self.BirthDate,
            'HireDate': self.HireDate,
            'Address': self.Address,
            'City': self.City,
            'Region': self.Region,
            'PostalCode': self.PostalCode,
            'Country': self.Country,
            'HomePhone': self.HomePhone,
            'Extension': self.Extension,
            'Notes': self.Notes,
            'ReportsTo': self.ReportsTo,
            'EmployeeType': self.EmployeeType,
            'Salary': float(self.Salary) if self.Salary else None,
            'Email': self.Email
        }



class Order(Base):
    """Order model for Northwind database"""
    __tablename__ = 'Order'
    
    Id = Column(Integer, primary_key=True)
    CustomerId = Column(String(8000), ForeignKey('Customer.Id'), nullable=False)
    EmployeeId = Column(Integer, ForeignKey('Employee.Id'), nullable=False)
    OrderDate = Column(String(8000))
    RequiredDate = Column(String(8000))
    ShippedDate = Column(String(8000))
    ShipVia = Column(Integer)
    Freight = Column(Numeric, default=0)
    ShipName = Column(String(8000))
    ShipAddress = Column(String(8000))
    ShipCity = Column(String(8000))
    ShipRegion = Column(String(8000))
    ShipPostalCode = Column(String(8000))
    ShipCountry = Column(String(8000))
    AmountTotal = Column(Numeric(10, 2))
    Country = Column(String(50))
    City = Column(String(50))
    Ready = Column(Integer)  # BOOLEAN stored as INTEGER in SQLite
    OrderDetailCount = Column(Integer, default=0)
    CloneFromOrder = Column(Integer, ForeignKey('Order.Id'))
    
    # Relationships
    customer = relationship("Customer", back_populates="orders")
    employee = relationship("Employee", back_populates="orders")
    order_details = relationship("OrderDetail", back_populates="order")
    
    def to_dict(self):
        return {
            'Id': self.Id,
            'CustomerId': self.CustomerId,
            'EmployeeId': self.EmployeeId,
            'OrderDate': self.OrderDate,
            'RequiredDate': self.RequiredDate,
            'ShippedDate': self.ShippedDate,
            'ShipVia': self.ShipVia,
            'Freight': float(self.Freight) if self.Freight else None,
            'ShipName': self.ShipName,
            'ShipAddress': self.ShipAddress,
            'ShipCity': self.ShipCity,
            'ShipRegion': self.ShipRegion,
            'ShipPostalCode': self.ShipPostalCode,
            'ShipCountry': self.ShipCountry,
            'AmountTotal': float(self.AmountTotal) if self.AmountTotal else None,
            'Country': self.Country,
            'City': self.City,
            'Ready': bool(self.Ready) if self.Ready is not None else None,
            'OrderDetailCount': self.OrderDetailCount
        }

class OrderDetail(Base):
    """Order Detail model for Northwind database"""
    __tablename__ = 'OrderDetail'
    
    Id = Column(Integer, primary_key=True)
    OrderId = Column(Integer, ForeignKey('Order.Id'), nullable=False)
    ProductId = Column(Integer, ForeignKey('Product.Id'), nullable=False)
    UnitPrice = Column(Numeric)
    Quantity = Column(Integer, nullable=False, default=1)
    Discount = Column(Numeric, default=0)
    Amount = Column(Numeric)
    ShippedDate = Column(String(8000))
    
    # Relationships
    order = relationship("Order", back_populates="order_details")
    product = relationship("Product", back_populates="order_details")
    
    def to_dict(self):
        return {
            'Id': self.Id,
            'OrderId': self.OrderId,
            'ProductId': self.ProductId,
            'UnitPrice': float(self.UnitPrice) if self.UnitPrice else None,
            'Quantity': self.Quantity,
            'Discount': float(self.Discount) if self.Discount else None,
            'Amount': float(self.Amount) if self.Amount else None,
            'ShippedDate': self.ShippedDate
        }
