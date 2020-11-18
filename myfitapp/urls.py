from django.urls import path

from .views import PDFGenerator, EmailJob, ReportView


app_name = "myfitapp"


urlpatterns = [
    path('generate-pdf/', PDFGenerator.as_view()),
    path('generate-email/', EmailJob.as_view()),
    path('report/', ReportView.as_view()),
]