# coding: utf-8
from sqlalchemy import DECIMAL, DateTime  # API Logic Server GenAI assist
from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

########################################################################################################################
# Classes describing database for SqlAlchemy ORM, initially created by schema introspection.
#
# Alter this file per your database maintenance policy
#    See https://apilogicserver.github.io/Docs/Project-Rebuild/#rebuilding
#
# Created:  October 30, 2024 17:22:07
# Database: sqlite:////tmp/tmp.no9YhiFjJ6/Foo/database/db.sqlite
# Dialect:  sqlite
#
# mypy: ignore-errors
########################################################################################################################
 
from database.system.SAFRSBaseX import SAFRSBaseX
from flask_login import UserMixin
import safrs, flask_sqlalchemy
from safrs import jsonapi_attr
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped
from sqlalchemy.sql.sqltypes import NullType
from typing import List

db = SQLAlchemy() 
Base = declarative_base()  # type: flask_sqlalchemy.model.DefaultMeta
metadata = Base.metadata

#NullType = db.String  # datatype fixup
#TIMESTAMP= db.TIMESTAMP

from sqlalchemy.dialects.sqlite import *



class Customer(SAFRSBaseX, Base):
    """
    description: Table to store customer details
    """
    __tablename__ = 'customer'
    _s_collection_name = 'Customer'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)
    balance = Column(Float)

    # parent relationships (access parent)

    # child relationships (access children)
    CartList : Mapped[List["Cart"]] = relationship(back_populates="customer")
    OrderList : Mapped[List["Order"]] = relationship(back_populates="customer")



class Product(SAFRSBaseX, Base):
    """
    description: Table to store information on golf clothing products
    """
    __tablename__ = 'product'
    _s_collection_name = 'Product'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    category = Column(String(50), nullable=False)
    unit_price = Column(Float, nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)
    InventoryList : Mapped[List["Inventory"]] = relationship(back_populates="product")
    ProductPromotionList : Mapped[List["ProductPromotion"]] = relationship(back_populates="product")
    SupplierProductList : Mapped[List["SupplierProduct"]] = relationship(back_populates="product")
    CartItemList : Mapped[List["CartItem"]] = relationship(back_populates="product")
    OrderItemList : Mapped[List["OrderItem"]] = relationship(back_populates="product")



class Promotion(SAFRSBaseX, Base):
    """
    description: Table to define promotions available in the store
    """
    __tablename__ = 'promotion'
    _s_collection_name = 'Promotion'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    discount_percentage = Column(Float, nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)
    ProductPromotionList : Mapped[List["ProductPromotion"]] = relationship(back_populates="promotion")



class Supplier(SAFRSBaseX, Base):
    """
    description: Table for suppliers providing products
    """
    __tablename__ = 'supplier'
    _s_collection_name = 'Supplier'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    contact_email = Column(String(100), nullable=False)

    # parent relationships (access parent)

    # child relationships (access children)
    SupplierProductList : Mapped[List["SupplierProduct"]] = relationship(back_populates="supplier")



class Cart(SAFRSBaseX, Base):
    """
    description: Table to store shopping cart details for customers
    """
    __tablename__ = 'cart'
    _s_collection_name = 'Cart'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customer.id'), nullable=False)
    created_date = Column(DateTime)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("CartList"))

    # child relationships (access children)
    CartItemList : Mapped[List["CartItem"]] = relationship(back_populates="cart")



class Inventory(SAFRSBaseX, Base):
    """
    description: Table to store product inventory details
    """
    __tablename__ = 'inventory'
    _s_collection_name = 'Inventory'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    product_id = Column(ForeignKey('product.id'), nullable=False)
    stock_quantity = Column(Integer, nullable=False)

    # parent relationships (access parent)
    product : Mapped["Product"] = relationship(back_populates=("InventoryList"))

    # child relationships (access children)



class Order(SAFRSBaseX, Base):
    """
    description: Table to store orders made by customers
    """
    __tablename__ = 'order'
    _s_collection_name = 'Order'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    customer_id = Column(ForeignKey('customer.id'), nullable=False)
    order_date = Column(DateTime)
    amount_total = Column(Float)

    # parent relationships (access parent)
    customer : Mapped["Customer"] = relationship(back_populates=("OrderList"))

    # child relationships (access children)
    OrderItemList : Mapped[List["OrderItem"]] = relationship(back_populates="order")
    PaymentList : Mapped[List["Payment"]] = relationship(back_populates="order")
    ShippingList : Mapped[List["Shipping"]] = relationship(back_populates="order")



class ProductPromotion(SAFRSBaseX, Base):
    """
    description: Junction table to associate products with promotions
    """
    __tablename__ = 'product_promotion'
    _s_collection_name = 'ProductPromotion'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    product_id = Column(ForeignKey('product.id'), nullable=False)
    promotion_id = Column(ForeignKey('promotion.id'), nullable=False)

    # parent relationships (access parent)
    product : Mapped["Product"] = relationship(back_populates=("ProductPromotionList"))
    promotion : Mapped["Promotion"] = relationship(back_populates=("ProductPromotionList"))

    # child relationships (access children)



class SupplierProduct(SAFRSBaseX, Base):
    """
    description: Junction table linking suppliers with their products
    """
    __tablename__ = 'supplier_product'
    _s_collection_name = 'SupplierProduct'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    supplier_id = Column(ForeignKey('supplier.id'), nullable=False)
    product_id = Column(ForeignKey('product.id'), nullable=False)

    # parent relationships (access parent)
    product : Mapped["Product"] = relationship(back_populates=("SupplierProductList"))
    supplier : Mapped["Supplier"] = relationship(back_populates=("SupplierProductList"))

    # child relationships (access children)



class CartItem(SAFRSBaseX, Base):
    """
    description: Junction table to store items in a shopping cart
    """
    __tablename__ = 'cart_item'
    _s_collection_name = 'CartItem'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    cart_id = Column(ForeignKey('cart.id'), nullable=False)
    product_id = Column(ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)

    # parent relationships (access parent)
    cart : Mapped["Cart"] = relationship(back_populates=("CartItemList"))
    product : Mapped["Product"] = relationship(back_populates=("CartItemList"))

    # child relationships (access children)



class OrderItem(SAFRSBaseX, Base):
    """
    description: Junction table to store items within an order
    """
    __tablename__ = 'order_item'
    _s_collection_name = 'OrderItem'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey('order.id'), nullable=False)
    product_id = Column(ForeignKey('product.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    amount = Column(Float, nullable=False)

    # parent relationships (access parent)
    order : Mapped["Order"] = relationship(back_populates=("OrderItemList"))
    product : Mapped["Product"] = relationship(back_populates=("OrderItemList"))

    # child relationships (access children)



class Payment(SAFRSBaseX, Base):
    """
    description: Table to store payment information for orders
    """
    __tablename__ = 'payment'
    _s_collection_name = 'Payment'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey('order.id'), nullable=False)
    payment_date = Column(DateTime)
    amount_paid = Column(Float, nullable=False)

    # parent relationships (access parent)
    order : Mapped["Order"] = relationship(back_populates=("PaymentList"))

    # child relationships (access children)



class Shipping(SAFRSBaseX, Base):
    """
    description: Table to handle shipping details for orders
    """
    __tablename__ = 'shipping'
    _s_collection_name = 'Shipping'  # type: ignore
    __bind_key__ = 'None'

    id = Column(Integer, primary_key=True)
    order_id = Column(ForeignKey('order.id'), nullable=False)
    address = Column(String(255), nullable=False)
    shipping_date = Column(DateTime)

    # parent relationships (access parent)
    order : Mapped["Order"] = relationship(back_populates=("ShippingList"))

    # child relationships (access children)
