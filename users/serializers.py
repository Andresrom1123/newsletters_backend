import os

from django.template.loader import render_to_string
from rest_framework import serializers
from sendgrid import Mail, SendGridAPIClient

from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'password']

    def create(self, validated_data):
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        rendered = render_to_string('email.html', {'user': user})
        message = Mail(
            from_email='newsletters@gmail.com',
            to_emails='amclres@gmail.com',
            subject='E-mail Confirmation',
            html_content=rendered)
        try:
            sg = SendGridAPIClient('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')
            response = sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e)

        return user
