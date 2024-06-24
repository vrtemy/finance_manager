from django.shortcuts import render, HttpResponse

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle

from finances.models import Transaction


def pdf_generation(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="transactions.pdf"'

    # Получение данных из модели Transaction
    user = request.user
    transactions = Transaction.objects.filter(user=user)

    # Создание PDF документа
    pdf = SimpleDocTemplate(response, pagesize=letter)
    elements = []

    # Определение стилей для таблицы
    style = getSampleStyleSheet()
    style_title = style["Title"]
    style_table = style["Normal"]
    style_table.alignment = 100

    # Формирование данных для таблицы в PDF
    data = [['Category', 'Sum', 'Date']]
    for transaction in transactions:
        data.append([transaction.category.name, transaction.sum, transaction.date])

    # Создание таблицы
    transactions_table = Table(data)
    transactions_table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                                            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                                            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                                            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                                            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                                            ('BACKGROUND', (0, 1), (-1, -1), colors.beige)]))
    elements.append(transactions_table)

    # Генерация PDF
    pdf.build(elements)
    return response
