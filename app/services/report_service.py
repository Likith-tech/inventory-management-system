from datetime import datetime, time

from app.models import Product, Sale


def sales_between(from_date, to_date):
    start = datetime.combine(from_date, time.min)
    end = datetime.combine(to_date, time.max)
    return Sale.query.filter(Sale.sale_date.between(start, end)).order_by(Sale.sale_date.desc()).all()


def low_stock_products():
    return Product.query.filter(Product.quantity <= Product.low_stock_limit).order_by(Product.quantity.asc()).all()


def sales_total(sales):
    return sum(sale.total_amount for sale in sales)
