# coding: utf8

from sqlalchemy import Column, ForeignKey, INTEGER, DATETIME, func
from sqlalchemy import VARCHAR, TEXT, CHAR
from sqlalchemy.orm import relationship

from packages.databases import base


class Categories(base.Base):
    __tablename__ = 'categories'
    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(150), nullable=False)
    link_http = Column(VARCHAR(250), nullable=False)
    id_category = Column(VARCHAR(150), nullable=True)


class Products(base.Base):
    __tablename__ = 'products'
    id = Column(INTEGER, primary_key=True)
    name = Column(VARCHAR(150), nullable=False)
    description = Column(TEXT, nullable=False)
    nutrition_grade = Column(CHAR(1), nullable=False)
    shop = Column(VARCHAR(100), nullable=True)
    link_http = Column(VARCHAR(250), nullable=False)
    categories = relationship("Categories", secondary="link_category_product")


class Link_category_product(base.Base):
    __tablename__ = 'link_category_product'

    category_id = Column(INTEGER, ForeignKey('categories.id'), primary_key=True)
    product_id = Column(INTEGER, ForeignKey('products.id'), primary_key=True)

    category = relationship("Categories", backref="categories_associations")
    product = relationship("Products", backref="products_associations")


class SaveProducts(base.Base):
    __tablename__ = 'save_products'
    id = Column(INTEGER, primary_key=True)
    id_product = Column(INTEGER, ForeignKey('products.id'), nullable=False)
    date = Column(DATETIME, default=func.now())
    save_product = relationship("Products", backref="save_products_associations", uselist=False)
