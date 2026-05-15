from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from app import db
from app.forms import ProductForm
from app.models import Category, Product, Supplier

bp = Blueprint('products', __name__, url_prefix='/products')


def load_product_choices(form):
    form.category_id.choices = [(c.id, c.name) for c in Category.query.order_by(Category.name).all()]
    form.supplier_id.choices = [(s.id, s.name) for s in Supplier.query.order_by(Supplier.name).all()]


@bp.route('/')
@login_required
def list_products():
    search = request.args.get('search', '').strip()
    query = Product.query
    if search:
        query = query.filter((Product.name.ilike(f'%{search}%')) | (Product.sku.ilike(f'%{search}%')))
    products = query.order_by(Product.name).all()
    return render_template('products/list.html', title='Products', products=products, search=search)


@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_product():
    if Category.query.count() == 0 or Supplier.query.count() == 0:
        flash('Please add at least one category and one supplier before adding products.', 'warning')
        return redirect(url_for('products.list_products'))

    form = ProductForm()
    load_product_choices(form)

    if form.validate_on_submit():
        product = Product(
            name=form.name.data,
            sku=form.sku.data,
            description=form.description.data,
            price=form.price.data,
            quantity=form.quantity.data,
            low_stock_limit=form.low_stock_limit.data,
            category_id=form.category_id.data,
            supplier_id=form.supplier_id.data,
        )
        db.session.add(product)
        db.session.commit()
        flash('Product added successfully.', 'success')
        return redirect(url_for('products.list_products'))

    return render_template('products/form.html', title='Add Product', form=form)


@bp.route('/<int:product_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_product(product_id):
    product = Product.query.get_or_404(product_id)
    form = ProductForm(obj=product)
    load_product_choices(form)

    if form.validate_on_submit():
        form.populate_obj(product)
        db.session.commit()
        flash('Product updated successfully.', 'success')
        return redirect(url_for('products.list_products'))

    return render_template('products/form.html', title='Edit Product', form=form)


@bp.route('/<int:product_id>/delete', methods=['POST'])
@login_required
def delete_product(product_id):
    product = Product.query.get_or_404(product_id)
    db.session.delete(product)
    db.session.commit()
    flash('Product deleted successfully.', 'info')
    return redirect(url_for('products.list_products'))
