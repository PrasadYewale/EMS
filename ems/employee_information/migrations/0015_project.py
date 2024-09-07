# Generated by Django 4.2 on 2023-05-01 14:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employee_information', '0014_point'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('employees_required', models.IntegerField()),
                ('categories', models.CharField(choices=[('accuracy', 'Accuracy'), ('speed', 'Speed')], max_length=10)),
            ],
        ),
    ]
