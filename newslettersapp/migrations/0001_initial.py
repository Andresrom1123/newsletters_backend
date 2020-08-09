# Generated by Django 2.2.14 on 2020-08-07 23:26

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_created=django.utils.timezone.now)),
                ('name', models.CharField(max_length=50)),
                ('description', models.CharField(max_length=100)),
                ('image', models.ImageField(upload_to='', verbose_name='Image Newsletter')),
                ('subscribe', models.IntegerField()),
                ('target', models.IntegerField()),
                ('frequency', models.CharField(max_length=50)),
                ('vote', models.BooleanField(default=False)),
                ('subscribed', models.BooleanField(default=False)),
            ],
        ),
    ]
