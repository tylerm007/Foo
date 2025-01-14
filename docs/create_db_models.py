# created from response - used to create database and project
#  should run without error
#  if not, check for decimal, indent, or import issues

import decimal

import logging



logging.getLogger('sqlalchemy.engine.Engine').disabled = True  # remove for additional logging

import sqlalchemy



from sqlalchemy.sql import func  # end imports from system/genai/create_db_models_inserts/create_db_models_prefix.py

from logic_bank.logic_bank import Rule

from sqlalchemy import create_engine, Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class Customer(Base):
    """
    description: Table to store customer details
    """
    __tablename__ = 'customer'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    balance = Column(Float, default=0.0)

class Product(Base):
    """
    description: Table to store information on golf clothing products
    """
    __tablename__ = 'product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    unit_price = Column(Float, nullable=False)

class Cart(Base):
    """
    description: Table to store shopping cart details for customers
    """
    __tablename__ = 'cart'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    created_date = Column(DateTime, default=datetime.datetime.now)

class CartItem(Base):
    """
    description: Junction table to store items in a shopping cart
    """
    __tablename__ = 'cart_item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    cart_id = Column(Integer, ForeignKey('cart.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)

class Order(Base):
    """
    description: Table to store orders made by customers
    """
    __tablename__ = 'order'
    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(Integer, ForeignKey('customer.id'), nullable=False)
    order_date = Column(DateTime, default=datetime.datetime.now)
    amount_total = Column(Float, default=0.0)

class OrderItem(Base):
    """
    description: Junction table to store items within an order
    """
    __tablename__ = 'order_item'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)

class Inventory(Base):
    """
    description: Table to store product inventory details
    """
    __tablename__ = 'inventory'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    stock_quantity = Column(Integer, nullable=False)

class Supplier(Base):
    """
    description: Table for suppliers providing products
    """
    __tablename__ = 'supplier'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    contact_email = Column(String(100), nullable=False)

class SupplierProduct(Base):
    """
    description: Junction table linking suppliers with their products
    """
    __tablename__ = 'supplier_product'
    id = Column(Integer, primary_key=True, autoincrement=True)
    supplier_id = Column(Integer, ForeignKey('supplier.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)

class Payment(Base):
    """
    description: Table to store payment information for orders
    """
    __tablename__ = 'payment'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    payment_date = Column(DateTime, default=datetime.datetime.now)
    amount_paid = Column(Float, nullable=False)

class Shipping(Base):
    """
    description: Table to handle shipping details for orders
    """
    __tablename__ = 'shipping'
    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    address = Column(String(255), nullable=False)
    shipping_date = Column(DateTime, nullable=True)

class Promotion(Base):
    """
    description: Table to define promotions available in the store
    """
    __tablename__ = 'promotion'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    discount_percentage = Column(Float, nullable=False)

class ProductPromotion(Base):
    """
    description: Junction table to associate products with promotions
    """
    __tablename__ = 'product_promotion'
    id = Column(Integer, primary_key=True, autoincrement=True)
    product_id = Column(Integer, ForeignKey('product.id'), nullable=False)
    promotion_id = Column(Integer, ForeignKey('promotion.id'), nullable=False)

# Set up the database
engine = create_engine('sqlite:///system/genai/temp/create_db_models.sqlite')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

# Sample data insertion
customer1 = Customer(name="John Doe", email="johndoe@example.com", balance=100.0)
customer2 = Customer(name="Jane Smith", email="janesmith@example.com", balance=150.0)

product1 = Product(name="Golf Shirt", category="Shirts", unit_price=50.0)
product2 = Product(name="Golf Pants", category="Pants", unit_price=70.0)
product3 = Product(name="Golf Cap", category="Accessories", unit_price=20.0)

cart1 = Cart(customer_id=1)
cart_item1 = CartItem(cart_id=1, product_id=1, quantity=2, amount=100.0)
cart_item2 = CartItem(cart_id=1, product_id=2, quantity=1, amount=70.0)

order1 = Order(customer_id=1, amount_total=170.0)
order_item1 = OrderItem(order_id=1, product_id=1, quantity=2, amount=100.0)
order_item2 = OrderItem(order_id=1, product_id=2, quantity=1, amount=70.0)

inventory1 = Inventory(product_id=1, stock_quantity=100)
inventory2 = Inventory(product_id=2, stock_quantity=200)

supplier1 = Supplier(name="Golf Supplier Co.", contact_email="contact@golfsupplier.com")
supplier_product1 = SupplierProduct(supplier_id=1, product_id=1)

payment1 = Payment(order_id=1, amount_paid=170.0)

shipping1 = Shipping(order_id=1, address="123 Golf Lane, Golftown, USA")

promotion1 = Promotion(name="Spring Sale", discount_percentage=10.0)
product_promotion1 = ProductPromotion(product_id=1, promotion_id=1)

# Adding data to session
session.add_all([
    customer1, customer2,
    product1, product2, product3,
    cart1, cart_item1, cart_item2,
    order1, order_item1, order_item2,
    inventory1, inventory2,
    supplier1, supplier_product1,
    payment1,
    shipping1,
    promotion1, product_promotion1
])

session.commit()
session.close()
