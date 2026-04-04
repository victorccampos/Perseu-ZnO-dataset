import smtplib
from email.message import EmailMessage
from datetime import datetime
import socket
import sys

import os
from dotenv import load_dotenv

load_dotenv()

APP_PASSWORD = os.getenv("APP_PASSWORD")
EMAIL_FROM = os.getenv("EMAIL_FROM")
EMAIL_TO = os.getenv("EMAIL_TO")


def send_email(subject, body):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_FROM
    msg["To"] = EMAIL_TO
    msg.set_content(body)

    with smtplib.SMTP("smtp.gmail.com", 587) as smtp:
        smtp.starttls()
        smtp.login(EMAIL_FROM, APP_PASSWORD)
        smtp.send_message(msg)


if __name__ == "__main__":
    status = sys.argv[1] if len(sys.argv) > 1 else "UNKNOWN"

    hostname = socket.gethostname()
    time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    subject = f"Job at {hostname}: ({status})"
    body = f"""
HOST: {hostname}
JOB NAME: "{status}"
TIME: {time}
"""

    send_email(subject, body)
