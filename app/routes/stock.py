from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import current_user, login_required

from app import db
from app.forms import StockInForm
from app.models import Product, StockIn, Supplier
from app.services.inventory_service import add_stock
from app.services.activity_service import log_activity
from app.services.notification_service import notify_role_users

bp = Blueprint('stock', __name__, url_prefix='/stock')


@bp.route('/in', methods=['GET', 'POST'])
@login_required
def stock_in():
    form = StockInForm()
    form.product_id.choices = [(p.id, f'{p.name} ({p.sku})') for p in Product.query.order_by(Product.name).all()]
    form.supplier_id.choices = [(s.id, s.name) for s in Supplier.query.order_by(Supplier.name).all()]

    if form.validate_on_submit():
        stock_entry = add_stock(
            form.product_id.data,
            form.supplier_id.data,
            form.quantity.data,
            form.note.data,
            current_user.id,
            commit=False,
        )

        product = Product.query.get(form.product_id.data)
        supplier = Supplier.query.get(form.supplier_id.data)
        log_activity(
            current_user.id,
            'CREATE',
            'StockIn',
            stock_entry.id,
            f'Added {form.quantity.data} units of {product.name} from {supplier.name}',
        )
        if product.quantity <= product.low_stock_limit:
            notify_role_users(
                ['admin', 'manager'],
                f'Low stock: {product.name} has {product.quantity} units left after stock update.',
                'warning',
            )
        db.session.commit()

        flash('Stock added and product quantity updated.', 'success')
        return redirect(url_for('stock.stock_in'))

    entries = StockIn.query.order_by(StockIn.created_at.desc()).limit(20).all()
    return render_template('stock/stock_in.html', title='Incoming Stock', form=form, entries=entries)
