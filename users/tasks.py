from django.template.loader import render_to_string

from newsletters.celery import app
from sendgrid import Mail, SendGridAPIClient


@app.task(name='send_email')
def send_email(email):
    rendered = render_to_string('staff.html')
    msg = Mail(
        from_email='newsletters@gmail.com',
        to_emails=email,
        subject='Newsletter Staff',
        html_content=rendered)
    sg = SendGridAPIClient('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')
    sg.send(msg)


@app.task(name='send_email_user')
def send_email_user(email, token):
    rendered = render_to_string('email.html', {'token': token})
    message = Mail(
        from_email='newsletters@gmail.com',
        to_emails=email,
        subject='Email Confirmation',
        html_content=rendered)
    try:
        sg = SendGridAPIClient('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')
        response = sg.send(message)
        print(response.status_code)
    except Exception as e:
        print(e)
