# Generated by Django 4.2.14 on 2024-12-29 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counting', '0005_worklog_bonus_minutes'),
    ]

    operations = [
        migrations.AddField(
            model_name='worklog',
            name='minutes_worked',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=5),
        ),
        migrations.AlterField(
            model_name='worklog',
            name='hours_worked',
            field=models.DecimalField(decimal_places=0, default=0, max_digits=5),
        ),
    ]