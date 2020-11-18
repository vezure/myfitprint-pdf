from pdfy import Pdfy
from django.conf import settings



def generate_pdf(access_hash):
    pdf_generator = None
    options = {'paperWidth': 8.5, 'paperHeight': 11.5, 'printBackground': True}
    if not pdf_generator:
        pdf_generator = get_pdfy_object()

    return pdf_generator.html_to_pdf(settings.INTERNAL_REPORT_URL.format(
        access_hash
    ),
        options=options)


def get_pdfy_object():
    pdf_generator = Pdfy(settings.CHROME_PATH)
    return pdf_generator
