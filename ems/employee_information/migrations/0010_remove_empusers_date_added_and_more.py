# Generated by Django 4.2 on 2023-04-30 09:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee_information', '0009_empusers_date_added_empusers_date_updated'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='empusers',
            name='date_added',
        ),
        migrations.RemoveField(
            model_name='empusers',
            name='date_updated',
        ),
    ]
