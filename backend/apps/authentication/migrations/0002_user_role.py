# Generated by Django 5.1.4 on 2024-12-09 23:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('patient', 'Patient'), ('doctor', 'Doctor'), ('clinic', 'Clinic')], default='patient', max_length=10),
        ),
    ]