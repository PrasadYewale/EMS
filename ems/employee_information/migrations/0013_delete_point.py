# Generated by Django 4.2 on 2023-04-30 19:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employee_information', '0012_remove_point_pointable_id_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Point',
        ),
    ]
