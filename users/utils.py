import smtplib
from email.message import EmailMessage

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = 'amithtalentplace@gmail.com'
EMAIL_HOST_PASSWORD = 'kxst rloj hbai yrpo' 
EMAIL_PORT = 587
EMAIL_USE_TLS = True
DEFAULT_FROM_EMAIL = 'amithtalentplace@gmail.com'


def send_password_email(to_email,password):
    subject = 'Your account Password'
    body = f'Your password is {password}'
    
    msg = EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_HOST_USER
    msg['To'] = to_email
    
    smtp_server = EMAIL_HOST
    smtp_port = 587
    smtp_user = EMAIL_HOST_USER
    smtp_password = EMAIL_HOST_PASSWORD
    
    with smtplib.SMTP(smtp_server, smtp_user) as server:
        server.starttls()
        server.login(smtp_user, smtp_password)
        server.send_message(msg)
        
    print(f'Email sent to {to_email} with password: {password}')