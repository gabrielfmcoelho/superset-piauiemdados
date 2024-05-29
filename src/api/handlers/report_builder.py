from fpdf import FPDF, HTMLMixin
from jinja2 import Template
from io import BytesIO
import os

class PDF(FPDF, HTMLMixin):
    pass

def build_report(report_data):
    print("Building report...")
    pdf = PDF()
    pdf.add_page()

    print(os.getcwd())
    print(os.listdir("templates"))
    with open('templates/report.html', 'r') as file:
        template = Template(file.read())
    
    html_content = template.render(
        title=report_data['title'],
        subtitle=report_data['subtitle'],
        #map=report_data.get('map', ''),
        data=report_data['data']
    )

    pdf.write_html(html_content)

    pdf_output = BytesIO()
    pdf.output(pdf_output, 'F')
    pdf_output.seek(0)

    return pdf_output
