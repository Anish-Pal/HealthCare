# Generated by Django 5.1.7 on 2025-05-28 16:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_alter_hospital_display'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='name',
            field=models.CharField(choices=[('ENT', 'ENT'), ('CARDIOLOGY', 'Cardiology'), ('ORTHO', 'Orthopedics'), ('PEDIATRICS', 'Pediatrics'), ('GASTROENTEROLOGY', 'Gastroenterology'), ('NEUROLOGY', 'Neurology'), ('GYNECOLOGY', 'Gynecology & Obstetrics'), ('DERMATOLOGY', 'Dermatology'), ('ONCOLOGY', 'Oncology'), ('NEPHROLOGY', 'Nephrology'), ('PULMONOLOGY', 'Pulmonology'), ('OPHTHALMOLOGY', 'Ophthalmology')], max_length=50),
        ),
    ]
