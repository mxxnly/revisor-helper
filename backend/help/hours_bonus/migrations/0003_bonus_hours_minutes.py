# Generated by Django 4.2.14 on 2024-12-31 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hours_bonus', '0002_bonus_hours_year_alter_bonus_hours_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='bonus_hours',
            name='minutes',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]