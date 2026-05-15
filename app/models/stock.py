from datetime import datetime

from app import db


class StockIn(db.Model):
    __tablename__ = 'stock_in'

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'))
    quantity = db.Column(db.Integer, nullable=False)
    note = db.Column(db.String(255))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    product = db.relationship('Product', back_populates='stock_entries')
    supplier = db.relationship('Supplier', back_populates='stock_entries')
    user = db.relationship('User')
