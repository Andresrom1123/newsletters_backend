from django.template.loader import render_to_string
from sendgrid import Mail, SendGridAPIClient

from newsletters.celery import app


@app.task(name='send_email_newsletter')
def send_email_newsletter(users, newsletter):
    rendered = render_to_string('newsletter.html', {'newsletter': newsletter})
    for user in users:
        msg = Mail(
            from_email='newsletters@gmail.com',
            to_emails=user.get('email'),
            subject='Newsletter Staff',
            html_content=rendered)
        sg = SendGridAPIClient('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')
        sg.send(msg)
