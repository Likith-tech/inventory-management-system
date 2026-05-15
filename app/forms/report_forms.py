from flask_wtf import FlaskForm
from wtforms import DateField, SelectField, SubmitField
from wtforms.validators import DataRequired


class ReportFilterForm(FlaskForm):
    report_type = SelectField(
        'Report Type',
        choices=[
            ('sales', 'Sales Report'),
            ('daily_sales', 'Daily Sales Report'),
            ('low_stock', 'Low Stock Report'),
        ],
    )
    from_date = DateField('From Date', validators=[DataRequired()])
    to_date = DateField('To Date', validators=[DataRequired()])
    submit = SubmitField('Filter')
