from datetime import datetime
from email.mime.application import MIMEApplication
import base64

from django.conf import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import boto3

from .pdf_generation import generate_pdf


def send_email(acces_hash,to_addr, receiver_name, report_link):
    email_conn = None
    message = MIMEMultipart()
    message["From"] = settings.FROM_ADDR
    message["To"] = to_addr
    message["Subject"] = settings.EMAIL_SUBJECT
    encoded = base64.b64encode(open(settings.METFLUX_JPEG_PATH, "rb").read()).decode()
    body = settings.EMAIL_BODY.format(
        receiver_name, report_link, encoded)

    message.attach(MIMEText(body, "html"))
    pdf = MIMEApplication(base64.b64decode(generate_pdf(acces_hash)),
                          _subtype="pdf")
    pdf.add_header('Content-Disposition', 'attachment',
                   filename="MyFitPrint_{}.pdf".\
                   format(datetime.today().strftime("%d-%m-%Y")))
    message.attach(pdf)

    if not email_conn:
        email_conn = establish_email_connection()

    response = email_conn.send_raw_email(
        Source=message['From'],
        Destinations=[to_addr],
        RawMessage={
            'Data': message.as_string()
        }
    )


def establish_email_connection():

    client = boto3.client(
        'ses',
        region_name=settings.EMAIL_REGION_NAME,
        aws_access_key_id=settings.EMAIL_SECRET_KEY_ID,
        aws_secret_access_key=settings.EMAIL_SECRET_KEY
    )

    return client





