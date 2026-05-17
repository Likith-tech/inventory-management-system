from app import db
from app.models import Product, Sale, StockIn
from app.services.email_service import send_low_stock_alert


def add_stock(product_id, supplier_id, quantity, note, user_id, *, commit=True):
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
    db.session.flush()
    if commit:
        db.session.commit()
    return stock_entry


def record_sale(product_id, quantity, selling_price, user_id, customer_id=None, *, commit=True):
    """Decrease product stock after checking enough quantity exists."""
    product = Product.query.get_or_404(product_id)

    if quantity > product.quantity:
        raise ValueError('Sale quantity cannot be greater than available stock.')

    product.quantity -= quantity
    sale = Sale(
        product_id=product_id,
        customer_id=customer_id,
        quantity=quantity,
        selling_price=selling_price,
        total_amount=quantity * selling_price,
        created_by=user_id,
    )
    db.session.add(sale)
    db.session.flush()

    should_alert = product.quantity <= product.low_stock_limit
    if commit:
        db.session.commit()

    if should_alert:
        send_low_stock_alert(product.name, product.quantity, product.low_stock_limit)

    return sale
