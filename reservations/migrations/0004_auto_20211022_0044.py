# Generated by Django 3.2.6 on 2021-10-22 00:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reservations', '0003_bookedday'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='BookedDay',
            new_name='BetweenDay',
        ),
        migrations.AlterModelOptions(
            name='betweenday',
            options={'verbose_name': 'Booked Day', 'verbose_name_plural': 'Booked Days'},
        ),
    ]
