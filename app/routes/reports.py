from datetime import date

from flask import Blueprint, render_template, request
from flask_login import login_required

from app.forms import ReportFilterForm
from app.services.export_service import sales_csv_response, sales_pdf_response
from app.services.report_service import low_stock_products, sales_between, sales_total

bp = Blueprint('reports', __name__, url_prefix='/reports')


@bp.route('/', methods=['GET', 'POST'])
@login_required
def index():
    form = ReportFilterForm()
    if request.method == 'GET':
        form.from_date.data = date.today()
        form.to_date.data = date.today()

    sales = []
    low_stock = []
    total = 0

    if form.validate_on_submit():
        if form.report_type.data == 'low_stock':
            low_stock = low_stock_products()
        else:
            sales = sales_between(form.from_date.data, form.to_date.data)
            total = sales_total(sales)

    return render_template('reports/reports.html', title='Reports', form=form, sales=sales, low_stock=low_stock, total=total)


@bp.route('/sales/export/<file_type>')
@login_required
def export_sales(file_type):
    from_date = date.fromisoformat(request.args.get('from_date', str(date.today())))
    to_date = date.fromisoformat(request.args.get('to_date', str(date.today())))
    sales = sales_between(from_date, to_date)
    total = sales_total(sales)

    if file_type == 'pdf':
        return sales_pdf_response(sales, total)
    return sales_csv_response(sales)
