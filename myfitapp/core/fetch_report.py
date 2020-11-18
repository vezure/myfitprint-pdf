import mysql.connector
from django.conf import settings
import json


def fetch_report_data(access_hash):
    db = None
    data = {}
    query = "Select report from HealthReports where access_hash='{}'".format(
        access_hash
    )
    if not db:
        db = establish_connection()
    cursor = db.cursor()
    cursor.execute(query)
    records = cursor.fetchall()
    if records and json.loads(records[0][0]).get("comprehensive"):
        data = json.loads(records[0][0]).get("comprehensive")
        return data
    return data


def establish_connection():
    metflux_database = mysql.connector.connect(
        host=settings.MYSQL_HOST,
        user=settings.MYSQL_USER,
        password=settings.MYSQL_PASSWORD,
        port=settings.MYSQL_PORT,
        database=settings.MYSQL_DATABASE

    )

    return metflux_database
