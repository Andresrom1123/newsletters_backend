import os

from django.template.loader import render_to_string

from newsletters.celery import app
from sendgrid import Mail, SendGridAPIClient


@app.task(name='email-task')
def send_mail(email):
    rendered = render_to_string('staff.html')
    msg = Mail(
        from_email='newsletters@gmail.com',
        to_emails=email,
        subject='E-mail Confirmation',
        html_content=rendered)
    sg = SendGridAPIClient(os.getenv('SENDGRID_KEY'))
    sg.send(msg)
