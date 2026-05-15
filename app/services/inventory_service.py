from app import db
from app.models import Product, Sale, StockIn


def add_stock(product_id, supplier_id, quantity, note, user_id):
    """Increase product stock and save a stock-in history record."""
    product = Product.query.get_or_404(product_id)
    product.quantity += quantity

    stock_entry = StockIn(
        product_id=product_id,
        supplier_id=supplier_id,
        quantity=quantity,
        note=note,
        created_by=user_id,
    )
    db.session.add(stock_entry)
    db.session.commit()
    return stock_entry


def record_sale(product_id, quantity, selling_price, user_id):
    """Decrease product stock after checking enough quantity exists."""
    product = Product.query.get_or_404(product_id)

    if quantity > product.quantity:
        raise ValueError('Sale quantity cannot be greater than available stock.')

    product.quantity -= quantity
    sale = Sale(
        product_id=product_id,
        quantity=quantity,
        selling_price=selling_price,
        total_amount=quantity * selling_price,
        created_by=user_id,
    )
    db.session.add(sale)
    db.session.commit()
    return sale
