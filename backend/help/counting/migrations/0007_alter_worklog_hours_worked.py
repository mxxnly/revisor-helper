# Generated by Django 4.2.14 on 2024-12-29 19:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counting', '0006_worklog_minutes_worked_alter_worklog_hours_worked'),
    ]

    operations = [
        migrations.AlterField(
            model_name='worklog',
            name='hours_worked',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=5),
        ),
    ]
