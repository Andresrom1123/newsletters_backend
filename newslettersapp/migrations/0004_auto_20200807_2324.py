# Generated by Django 2.2.14 on 2020-08-07 23:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('newslettersapp', '0003_newslettersuser'),
    ]

    operations = [
        migrations.RenameField(
            model_name='newsletter',
            old_name='meta',
            new_name='subscribe',
        ),
        migrations.AddField(
            model_name='newsletter',
            name='author',
            field=models.ForeignKey(default=django.utils.timezone.now, on_delete=django.db.models.deletion.CASCADE, related_name='author_newsletter', to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='newsletter',
            name='subscribed',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='newsletter',
            name='user',
            field=models.ManyToManyField(null=True, related_name='user_newsletter', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='newsletter',
            name='vote',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='NewslettersUser',
        ),
    ]
