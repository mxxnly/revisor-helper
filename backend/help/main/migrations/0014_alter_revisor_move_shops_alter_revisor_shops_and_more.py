# Generated by Django 4.2.14 on 2024-08-17 16:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0013_alter_shop_last_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revisor',
            name='move_shops',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='revisor',
            name='shops',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='revisor',
            name='way_shops',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]