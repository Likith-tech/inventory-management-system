from flask_wtf import FlaskForm
from decimal import Decimal, InvalidOperation
from wtforms import DecimalField, IntegerField, SelectField, StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, Length, NumberRange, Optional


def decimal_filter(value):
    if value in (None, ''):
        return value
    try:
        return Decimal(str(value))
    except (InvalidOperation, ValueError):
        return value


class ProductForm(FlaskForm):
    name = StringField('Product Name', validators=[DataRequired()])
    sku = StringField('SKU', validators=[DataRequired()])
    barcode = StringField('Barcode / UPC', validators=[Optional(), Length(max=100)])
    description = TextAreaField('Description')
    price = DecimalField('Selling Price', places=2, validators=[DataRequired(), NumberRange(min=0)], filters=[decimal_filter])
    cost_price = DecimalField('Cost Price', places=2, validators=[DataRequired(), NumberRange(min=0)], default=0, filters=[decimal_filter])
    quantity = IntegerField('Opening Quantity', validators=[NumberRange(min=0)], default=0)
    low_stock_limit = IntegerField('Low Stock Limit', validators=[NumberRange(min=0)], default=10)
    category_id = SelectField('Category', coerce=int, validators=[DataRequired()])
    supplier_id = SelectField('Supplier', coerce=int, validators=[DataRequired()])
    submit = SubmitField('Save Product')
