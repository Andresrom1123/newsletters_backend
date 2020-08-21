from django.template.loader import render_to_string

from newsletters.celery import app
from sendgrid import Mail, SendGridAPIClient


@app.task(name='send_email')
def send_email():
    # rendered = render_to_string('staff.html')
    msg = Mail(
        from_email='newsletters@gmail.com',
        to_emails='amclres@gmail.com',
        subject='Newsletter Staff',
        html_content='<p>Prueba</p>')
    sg = SendGridAPIClient('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')
    sg.send(msg)
