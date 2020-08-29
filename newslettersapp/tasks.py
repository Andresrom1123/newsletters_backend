from django.core.mail import EmailMessage
from django.template.loader import render_to_string

from newsletters.celery import app


@app.task(name='send_email_newsletter')
def send_email_newsletter(users, newsletter):
    rendered = render_to_string('newsletter.html', {'newsletter': newsletter})
    for user in users:
        msg = EmailMessage(
            'Newsletter',
            rendered,
            'Newsletters <from@example.com>',
            [user.get('email')],
        )
        msg.content_subtype = 'html'
        msg.send()
