# Generated by Django 4.2 on 2023-04-30 09:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee_information', '0010_remove_empusers_date_added_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='empusers',
            old_name='emp_password',
            new_name='password',
        ),
    ]
