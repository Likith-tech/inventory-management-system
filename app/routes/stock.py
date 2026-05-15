from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.forms import StockInForm
from app.models import Product, StockIn, Supplier
from app.services.inventory_service import add_stock

bp = Blueprint('stock', __name__, url_prefix='/stock')


@bp.route('/in', methods=['GET', 'POST'])
@login_required
def stock_in():
    form = StockInForm()
    form.product_id.choices = [(p.id, f'{p.name} ({p.sku})') for p in Product.query.order_by(Product.name).all()]
    form.supplier_id.choices = [(s.id, s.name) for s in Supplier.query.order_by(Supplier.name).all()]

    if form.validate_on_submit():
        add_stock(form.product_id.data, form.supplier_id.data, form.quantity.data, form.note.data, current_user.id)
        flash('Stock added and product quantity updated.', 'success')
        return redirect(url_for('stock.stock_in'))

    entries = StockIn.query.order_by(StockIn.created_at.desc()).limit(20).all()
    return render_template('stock/stock_in.html', title='Incoming Stock', form=form, entries=entries)
