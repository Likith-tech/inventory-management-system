from datetime import datetime

from app import db


class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False, index=True)
    sku = db.Column(db.String(80), unique=True, nullable=False, index=True)
    description = db.Column(db.String(255))
    price = db.Column(db.Float, default=0.0)
    quantity = db.Column(db.Integer, default=0)
    low_stock_limit = db.Column(db.Integer, default=10)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    category = db.relationship('Category', back_populates='products')
    supplier = db.relationship('Supplier', back_populates='products')
    stock_entries = db.relationship('StockIn', back_populates='product', cascade='all, delete-orphan')
    sales = db.relationship('Sale', back_populates='product', cascade='all, delete-orphan')

    @property
    def is_low_stock(self):
        return self.quantity <= self.low_stock_limit
