from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from app import db
from app.forms import CategoryForm
from app.models import Category

bp = Blueprint('categories', __name__, url_prefix='/categories')


@bp.route('/')
@login_required
def list_categories():
    categories = Category.query.order_by(Category.name).all()
    return render_template('categories/list.html', title='Categories', categories=categories)


@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        category = Category(name=form.name.data, description=form.description.data)
        db.session.add(category)
        db.session.commit()
        flash('Category saved successfully.', 'success')
        return redirect(url_for('categories.list_categories'))
    return render_template('categories/form.html', title='Add Category', form=form)


@bp.route('/<int:category_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_category(category_id):
    category = Category.query.get_or_404(category_id)
    form = CategoryForm(obj=category)
    if form.validate_on_submit():
        form.populate_obj(category)
        db.session.commit()
        flash('Category updated successfully.', 'success')
        return redirect(url_for('categories.list_categories'))
    return render_template('categories/form.html', title='Edit Category', form=form)


@bp.route('/<int:category_id>/delete', methods=['POST'])
@login_required
def delete_category(category_id):
    category = Category.query.get_or_404(category_id)
    if category.products.count() > 0:
        flash('Cannot delete a category that is linked to products.', 'warning')
        return redirect(url_for('categories.list_categories'))

    db.session.delete(category)
    db.session.commit()
    flash('Category deleted successfully.', 'info')
    return redirect(url_for('categories.list_categories'))
