# Generated by Django 3.2.6 on 2021-10-19 19:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='room',
            name='guests',
            field=models.IntegerField(help_text='총 몇 명이 예약하시나요??'),
        ),
        migrations.AlterField(
            model_name='room',
            name='host',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rooms', to=settings.AUTH_USER_MODEL),
        ),
    ]
