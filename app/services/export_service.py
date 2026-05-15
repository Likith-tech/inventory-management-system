import csv
import io

from flask import make_response
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def sales_csv_response(sales):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Date', 'Product', 'Quantity', 'Selling Price', 'Total'])

    for sale in sales:
        writer.writerow([
            sale.sale_date.strftime('%Y-%m-%d %H:%M'),
            sale.product.name,
            sale.quantity,
            sale.selling_price,
            sale.total_amount,
        ])

    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=sales_report.csv'
    response.headers['Content-Type'] = 'text/csv'
    return response


def sales_pdf_response(sales, total):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle('Sales Report')
    pdf.drawString(40, 750, 'Sales Report')
    pdf.drawString(40, 730, f'Total Sales Amount: {total:.2f}')

    y = 700
    for sale in sales:
        line = f'{sale.sale_date:%Y-%m-%d} | {sale.product.name} | Qty: {sale.quantity} | Total: {sale.total_amount:.2f}'
        pdf.drawString(40, y, line[:100])
        y -= 20
        if y < 60:
            pdf.showPage()
            y = 750

    pdf.save()
    buffer.seek(0)

    response = make_response(buffer.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=sales_report.pdf'
    response.headers['Content-Type'] = 'application/pdf'
    return response
