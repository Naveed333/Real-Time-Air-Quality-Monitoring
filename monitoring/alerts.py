import smtplib
from email.message import EmailMessage


def send_alert(message):
    msg = EmailMessage()
    msg.set_content(message)
    msg["Subject"] = "Air Quality Alert"
    msg["From"] = "alert@example.com"
    msg["To"] = "user@example.com"
    with smtplib.SMTP("localhost") as s:
        s.send_message(msg)
