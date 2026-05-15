from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app.forms import SaleForm
from app.models import Product, Sale
from app.services.inventory_service import record_sale

bp = Blueprint('sales', __name__, url_prefix='/sales')


@bp.route('/new', methods=['GET', 'POST'])
@login_required
def create_sale():
    form = SaleForm()
    form.product_id.choices = [(p.id, f'{p.name} - Stock: {p.quantity}') for p in Product.query.order_by(Product.name).all()]

    if form.validate_on_submit():
        try:
            record_sale(form.product_id.data, form.quantity.data, form.selling_price.data, current_user.id)
            flash('Sale saved and stock quantity updated.', 'success')
            return redirect(url_for('sales.create_sale'))
        except ValueError as error:
            flash(str(error), 'danger')

    sales = Sale.query.order_by(Sale.sale_date.desc()).limit(20).all()
    return render_template('sales/create_sale.html', title='Sales Entry', form=form, sales=sales)
