from datetime import date

from flask import Blueprint, render_template
from flask_login import login_required

from app.models import Category, Product, Sale, Supplier
from app.services.report_service import low_stock_products, sales_between, sales_total

bp = Blueprint('dashboard', __name__)


@bp.route('/')
@bp.route('/dashboard')
@login_required
def index():
    today_sales = sales_between(date.today(), date.today())
    stats = {
        'products': Product.query.count(),
        'categories': Category.query.count(),
        'suppliers': Supplier.query.count(),
        'today_sales': sales_total(today_sales),
        'low_stock': len(low_stock_products()),
        'transactions': Sale.query.count(),
    }
    return render_template('dashboard.html', title='Dashboard', stats=stats, low_stock_products=low_stock_products())
