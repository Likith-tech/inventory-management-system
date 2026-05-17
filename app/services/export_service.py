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


def inventory_csv_response(report_rows):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Product', 'SKU', 'Quantity', 'Price', 'Cost Price', 'Total Value', 'Total Cost'])

    for row in report_rows:
        writer.writerow([
            row['name'],
            row['sku'],
            row['quantity'],
            row['price'],
            row['cost_price'],
            row['total_value'],
            row['total_cost'],
        ])

    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=inventory_report.csv'
    response.headers['Content-Type'] = 'text/csv'
    return response


def inventory_pdf_response(report_rows, totals=None):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle('Inventory Report')
    pdf.drawString(40, 750, 'Inventory Report')
    y = 720
    if totals:
        pdf.drawString(40, 740, f"Total Inventory Value: {totals.get('value', 0):.2f}")
        y -= 20

    for row in report_rows:
        line = f"{row['name']} | SKU: {row['sku']} | Qty: {row['quantity']} | Value: {row['total_value']:.2f}"
        pdf.drawString(40, y, line[:100])
        y -= 18
        if y < 60:
            pdf.showPage()
            y = 750

    pdf.save()
    buffer.seek(0)
    response = make_response(buffer.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=inventory_report.pdf'
    response.headers['Content-Type'] = 'application/pdf'
    return response


def profit_csv_response(summary):
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Revenue', 'Cost', 'Profit'])
    writer.writerow([summary['revenue'], summary['cost'], summary['profit']])
    response = make_response(output.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=profit_loss.csv'
    response.headers['Content-Type'] = 'text/csv'
    return response


def profit_pdf_response(summary):
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=letter)
    pdf.setTitle('Profit and Loss Summary')
    pdf.drawString(40, 750, 'Profit and Loss Summary')
    pdf.drawString(40, 720, f"Revenue: {summary['revenue']:.2f}")
    pdf.drawString(40, 700, f"Cost: {summary['cost']:.2f}")
    pdf.drawString(40, 680, f"Profit: {summary['profit']:.2f}")
    pdf.save()
    buffer.seek(0)
    response = make_response(buffer.getvalue())
    response.headers['Content-Disposition'] = 'attachment; filename=profit_loss.pdf'
    response.headers['Content-Type'] = 'application/pdf'
    return response
