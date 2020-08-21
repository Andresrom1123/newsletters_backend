import os

from django.template.loader import render_to_string
from rest_framework import serializers
from sendgrid import Mail, SendGridAPIClient

from users.models import CustomUser


class UserCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name', 'email', 'password', 'token', 'is_active']

    def create(self, validated_data):
        user = CustomUser(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        rendered = render_to_string('email.html', {'user': user})
        message = Mail(
            from_email='newsletters@gmail.com',
            to_emails=user.email,
            subject='E-mail Confirmation',
            html_content=rendered)
        try:
            sg = SendGridAPIClient(os.getenv('SENDGRID_KEY'))
            response = sg.send(message)
            print(response.status_code)
        except Exception as e:
            print(e)

        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'first_name', 'last_name']
