import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

load_dotenv()

def send_email(subject: str, body: str, receiver_email: str):
    sender_email = os.environ["sender_email"]
    app_password = os.environ["app_password"]

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    message.attach(MIMEText(body, "plain"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, app_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        print("✅ Email sent successfully!")
        server.quit()
    except Exception as e:
        print("❌ Error sending email:", str(e))
