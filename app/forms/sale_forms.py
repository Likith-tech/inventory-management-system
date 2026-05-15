from flask_wtf import FlaskForm
from wtforms import FloatField, IntegerField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class SaleForm(FlaskForm):
    product_id = SelectField('Product', coerce=int, validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired(), NumberRange(min=1)])
    selling_price = FloatField('Selling Price', validators=[DataRequired(), NumberRange(min=0)])
    submit = SubmitField('Save Sale')
