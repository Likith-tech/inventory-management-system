from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from app import db
from app.forms import SupplierForm
from app.models import Supplier

bp = Blueprint('suppliers', __name__, url_prefix='/suppliers')


@bp.route('/')
@login_required
def list_suppliers():
    suppliers = Supplier.query.order_by(Supplier.name).all()
    return render_template('suppliers/list.html', title='Suppliers', suppliers=suppliers)


@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_supplier():
    form = SupplierForm()
    if form.validate_on_submit():
        supplier = Supplier(
            name=form.name.data,
            email=form.email.data,
            phone=form.phone.data,
            address=form.address.data,
        )
        db.session.add(supplier)
        db.session.commit()
        flash('Supplier saved successfully.', 'success')
        return redirect(url_for('suppliers.list_suppliers'))
    return render_template('suppliers/form.html', title='Add Supplier', form=form)


@bp.route('/<int:supplier_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    form = SupplierForm(obj=supplier)
    if form.validate_on_submit():
        form.populate_obj(supplier)
        db.session.commit()
        flash('Supplier updated successfully.', 'success')
        return redirect(url_for('suppliers.list_suppliers'))
    return render_template('suppliers/form.html', title='Edit Supplier', form=form)


@bp.route('/<int:supplier_id>/delete', methods=['POST'])
@login_required
def delete_supplier(supplier_id):
    supplier = Supplier.query.get_or_404(supplier_id)
    if supplier.products.count() > 0:
        flash('Cannot delete a supplier that is linked to products.', 'warning')
        return redirect(url_for('suppliers.list_suppliers'))

    db.session.delete(supplier)
    db.session.commit()
    flash('Supplier deleted successfully.', 'info')
    return redirect(url_for('suppliers.list_suppliers'))
