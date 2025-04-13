import smtplib
from email.message import EmailMessage
from django.conf import settings


def send_password_email(to_email,password):
    subject = 'Your account Password'
    body = f'Your password is {password}, You can login with either Phone Number or Email'
    
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = to_email
    
    smtp_server = settings.EMAIL_HOST
    smtp_port = settings.EMAIL_PORT
    smtp_user = settings.EMAIL_HOST_USER
    smtp_password = settings.EMAIL_HOST_PASSWORD
    
    with smtplib.SMTP(smtp_server, smtp_user) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        
    print(f'Email sent to {to_email} with password: {password}')