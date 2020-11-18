from datetime import datetime
from wsgiref.util import FileWrapper

from django.http import HttpResponse
from django.shortcuts import render
import io as BytesIO
import base64

# Create your views here.
from django.template.response import TemplateResponse
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import render
from django.template import Context
from django.template.loader import get_template

from .core.fetch_report import fetch_report_data
from .core.pdf_generation import generate_pdf
from .core.send_email import send_email


class PDFGenerator(APIView):

    def get(self, request):
        access_hash = request.GET.get('access_hash', '')
        if access_hash == '':
            return Response({"message": "Field access_hash is missing"})

        pdf_generated = generate_pdf(access_hash)
        buffer = BytesIO.BytesIO()
        content = base64.b64decode(pdf_generated)
        buffer.write(content)

        response = HttpResponse(
            buffer.getvalue(),
            content_type='application/pdf')
        response['Content-Disposition'] = 'inline; ' \
                                          'filename="MyFitPrint_{}.pdf"'. \
            format(datetime.today().strftime("%d-%m-%Y"))

        return response


class EmailJob(APIView):

    def get(self, request):
        access_hash = request.GET.get('access_hash', '')
        to_addr = request.GET.get('receiver_email', '')
        receiver_name = request.GET.get('receiver_name', '')
        report_link = request.GET.get('report_link', '')

        if access_hash == '' or to_addr == '' or receiver_name == '' \
                and report_link == '':
            return Response({"message": "Either of this fields are"
                                        " missing(access_hash, receiver_email,"
                                        "receiver_name, report_link)"})
        send_email(access_hash, to_addr, receiver_name, report_link)
        return Response({"message": "Email job success"})


class ReportView(APIView):

    def get(self, request):
        access_hash = request.GET.get('access_hash', '')
        data = fetch_report_data(access_hash)
        if data and data["sections"]:
            return render(request, "report.html",
                          dict(general=data["sections"][0],
                               diet_analysis=data["sections"][1],
                               weight_analysis=data["sections"][3],
                               your_scores=data["sections"][4],
                               risk=data["sections"][5],
                               goals=data["sections"][6],
                               diet_advice=data["sections"][7],
                               activity_advice=data["sections"][8],
                               lifestyle_advice=data["sections"][9],
                               definations=data["sections"][10])
                          )
        return Response({"message": "PDF generation Failed"})
