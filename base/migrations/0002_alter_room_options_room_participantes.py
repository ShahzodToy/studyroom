# Generated by Django 5.0.3 on 2024-04-01 10:27

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='room',
            options={'ordering': ['-created']},
        ),
        migrations.AddField(
            model_name='room',
            name='participantes',
            field=models.ManyToManyField(related_name='participantes', to=settings.AUTH_USER_MODEL),
        ),
    ]
