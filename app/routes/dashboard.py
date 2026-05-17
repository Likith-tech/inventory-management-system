from datetime import date, datetime

from flask import Blueprint, render_template
from flask_login import login_required
from app.utils.permissions import roles_required

from sqlalchemy import func

from app import db
from app.models import Category, Customer, Product, Sale, Supplier
from app.services.report_service import low_stock_products
from app.services.dashboard_service import (
    get_monthly_sales_data, get_inventory_status, get_top_selling_products,
    get_category_distribution, get_recent_activity, get_reorder_suggestions,
)
import json

bp = Blueprint('dashboard', __name__)


@bp.route('/')
@bp.route('/dashboard')
@login_required
@roles_required('admin', 'manager')
def index():
    # Basic stats
    total_products = Product.query.count()
    total_categories = Category.query.count()
    total_suppliers = Supplier.query.count()
    total_customers = Customer.query.count()
    total_sales = db.session.query(func.coalesce(func.sum(Sale.total_amount), 0)).scalar() or 0
    inventory_value = db.session.query(func.coalesce(func.sum(Product.quantity * Product.price), 0)).scalar() or 0
    low_stock_count = Product.query.filter(Product.quantity <= Product.low_stock_limit).count()
    recent_transactions = Sale.query.order_by(Sale.sale_date.desc()).limit(10).all()
    low_stock_products_list = low_stock_products()

    # Dashboard analytics
    monthly_labels, monthly_revenue = get_monthly_sales_data()
    inventory_status_labels, inventory_status_values = get_inventory_status()
    top_product_labels, top_product_values = get_top_selling_products()
    category_labels, category_values = get_category_distribution()
    recent_activity = get_recent_activity()
    reorder_suggestions = get_reorder_suggestions()

    chart_data = {
        'monthly_labels': monthly_labels,
        'monthly_revenue': monthly_revenue,
        'top_product_labels': top_product_labels,
        'top_product_values': top_product_values,
        'category_labels': category_labels,
        'category_values': category_values,
        'inventory_status_labels': inventory_status_labels,
        'inventory_status_values': inventory_status_values,
    }

    stats = {
        'total_products': total_products,
        'total_categories': total_categories,
        'total_suppliers': total_suppliers,
        'total_customers': total_customers,
        'total_sales': total_sales,
        'inventory_value': inventory_value,
        'low_stock_count': low_stock_count,
    }

    return render_template(
        'dashboard.html',
        stats=stats,
        recent_transactions=recent_transactions,
        low_stock_products=low_stock_products_list,
        chart_data=chart_data,
        recent_activity=recent_activity,
        reorder_suggestions=reorder_suggestions,
    )
    
