from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from newsletters.celery import app


@app.task(name='send_email')
def send_email(email):
    rendered = render_to_string('staff.html')
    msg = EmailMessage(
        'Newsletter Admin',
        rendered,
        'Newsletters <from@example.com>',
        [email],
    )
    msg.content_subtype = 'html'
    msg.send()


@app.task(name='send_email_user')
def send_email_user(email, token):
    rendered = render_to_string('email.html', {'token': token})
    msg = EmailMessage(
        'Confirm Email',
        rendered,
        'Newsletters <from@example.com>',
        [email],
    )
    try:
        msg.content_subtype = 'html'
        msg.send()
    except Exception as error:
        print(error)


@app.task(name='send_email_reset_password')
def send_email_reset_password(email, token):
    rendered = render_to_string('reset_password.html', {'token': token})
    msg = EmailMessage(
        'Reset Password',
        rendered,
        'Newsletters <from@example.com>',
        [email],
    )
    msg.content_subtype = 'html'
    msg.send()
