# Generated by Django 4.2.14 on 2024-09-10 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0032_merge_20240901_1628'),
    ]

    operations = [
        migrations.AddField(
            model_name='shop',
            name='avg_rating',
            field=models.FloatField(blank=True, null=True),
        ),
    ]