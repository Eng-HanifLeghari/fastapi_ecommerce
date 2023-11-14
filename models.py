from sqlalchemy import create_engine, Column, Integer, String, Float, Date, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func

Base = declarative_base()


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    description = Column(String(255))
    category = Column(String(255))  # Add the 'category' column here

    inventory = relationship("Inventory", back_populates="product")
    sales = relationship("Sale", back_populates="product")


class Sale(Base):
    __tablename__ = "sales"

    id = Column(Integer, primary_key=True, index=True)
    sale_date = Column(Date)
    quantity = Column(Integer)
    revenue = Column(Float)

    product_id = Column(Integer, ForeignKey("products.id"))
    product = relationship("Product", back_populates="sales")


class Inventory(Base):
    __tablename__ = 'inventory'

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    alert_threshold = Column(Integer)
    # Add other inventory-related fields as needed
    product = relationship("Product", back_populates="inventory")


class Promotion(Base):
    __tablename__ = 'promotions'

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String(255))
    discount = Column(Float)
    # Add other promotion-related fields as needed

# Define other tables if necessary (e.g., Customer, Order, etc.)
