# Generated by Django 2.2.14 on 2020-08-27 17:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('newslettersapp', '0002_auto_20200827_1729'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newsletter',
            old_name='user',
            new_name='users',
        ),
    ]
