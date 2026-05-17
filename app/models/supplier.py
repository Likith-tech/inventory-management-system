from app import db
from app.models.types import UTCDateTime
from app.utils.datetime import utc_now


class Supplier(db.Model):
    __tablename__ = 'suppliers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120))
    phone = db.Column(db.String(30))
    address = db.Column(db.String(255))
    created_at = db.Column(UTCDateTime(), default=utc_now)

    products = db.relationship('Product', back_populates='supplier', lazy='dynamic')
    stock_entries = db.relationship('StockIn', back_populates='supplier', lazy='dynamic')
