from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from django.core.files import File

def generate_pdf_report(data):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    
    elements = []
    elements.append(Paragraph("Personalized Meal Plan", styles['Title']))
    
    # Nutritional Summary Table
    summary_data = [
        ['Calories', 'Protein (g)', 'Carbs (g)', 'Fat (g)'],
        [
            data['Calories (kcal)'].sum(),
            data['Protein (g)'].sum(),
            data['Carbohydrates (g)'].sum(),
            data['Fat (g)'].sum()
        ]
    ]
    summary_table = Table(summary_data)
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), '#CCCCCC'),
        ('ALIGN', (0,0), (-1,-1), 'CENTER')
    ]))
    elements.append(summary_table)
    
    # Meal Details
    elements.append(Paragraph("Daily Meals:", styles['Heading2']))
    meal_data = [['Day', 'Meal Type', 'Food Item', 'Calories']]
    for idx, row in data.iterrows():
        meal_data.append([row['Date'], row['Meal_Type'], row['Food_Item'], row['Calories (kcal)']])
    
    meal_table = Table(meal_data)
    meal_table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), '#EEEEEE'),
        ('FONTSIZE', (0,0), (-1,0), 10),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE')
    ]))
    elements.append(meal_table)
    
    doc.build(elements)
    buffer.seek(0)
    return File(buffer, 'meal_plan.pdf')