import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from django.conf import settings


def send_mail(email, first_name, username, site_url, password, check, sub_domain):
    base_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    me = settings.EMAIL_HOST_USER
    email_password = settings.EMAIL_HOST_PASSWORD

    msg = MIMEMultipart('alternative')
    if check == 'forgot':
        msg['Subject'] = f'Forgot Password - Money Manager'
    else:
        msg['Subject'] = f'Welcome To Money Manager'

    msg['Message-ID'] = 'Welcome'

    path = fr'{base_path}/templates/mail/mail.html'
    if check == 'forgot':
        path = fr'{base_path}/templates/mail/forgot.html'

    with open(path, 'r') as f:
        html = f.read()
    html = html. \
        replace('{firstname_val}', f'<b>{first_name}</b>'). \
        replace('{username_val}', username). \
        replace('{email_val}', email). \
        replace('{password_val}', password). \
        replace('{siteurl_val}', site_url)

    part2 = MIMEText(html, 'html')

    msg.attach(part2)
    msg['From'] = f'Support Team {me}'
    msg['To'] = email
    mail = smtplib.SMTP('smtp.gmail.com', 587)

    mail.ehlo()

    mail.starttls()

    mail.login(f'{me}', f'{email_password}')
    mail.sendmail(me, email, msg.as_string())
    mail.quit()
