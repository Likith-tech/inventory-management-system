from flask_wtf import FlaskForm
from wtforms import IntegerField, SelectField, SubmitField, TextAreaField
from wtforms.validators import DataRequired, NumberRange


class StockInForm(FlaskForm):
    product_id = SelectField('Product', coerce=int, validators=[DataRequired()])
    supplier_id = SelectField('Supplier', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    note = TextAreaField('Note')
    submit = SubmitField('Add Stock')
