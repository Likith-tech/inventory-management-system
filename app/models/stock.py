from app import db
from app.models.types import UTCDateTime
from app.utils.datetime import utc_now


class StockIn(db.Model):
    __tablename__ = 'stock_in'
    __table_args__ = (
        db.CheckConstraint('quantity > 0', name='ck_stock_in_quantity_positive'),
        db.Index('ix_stock_in_product_created', 'product_id', 'created_at'),
    )

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, index=True)
    supplier_id = db.Column(db.Integer, db.ForeignKey('suppliers.id'), index=True)
    quantity = db.Column(db.Integer, nullable=False)
    note = db.Column(db.String(255))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), index=True)
    created_at = db.Column(UTCDateTime(), default=utc_now, index=True)

    product = db.relationship('Product', back_populates='stock_entries')
    supplier = db.relationship('Supplier', back_populates='stock_entries')
    user = db.relationship('User')
