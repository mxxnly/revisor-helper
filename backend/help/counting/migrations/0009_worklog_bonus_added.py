# Generated by Django 4.2.14 on 2025-01-02 23:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('counting', '0008_remove_worklog_bonus_minutes'),
    ]

    operations = [
        migrations.AddField(
            model_name='worklog',
            name='bonus_added',
            field=models.BooleanField(default=False),
        ),
    ]
