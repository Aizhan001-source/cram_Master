import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(to_email, link):
    sender_email = "khhaii@mail.ru"
    password = "XT64xkRB4lJENyqLGEP1"  # ⚠️ не обычный пароль!

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = to_email
    msg["Subject"] = "Password Reset"

    body = f"Reset your password:\n{link}"
    msg.attach(MIMEText(body, "plain"))

    with smtplib.SMTP_SSL("smtp.mail.ru", 465) as server:
        server.login(sender_email, password)
        server.send_message(msg)