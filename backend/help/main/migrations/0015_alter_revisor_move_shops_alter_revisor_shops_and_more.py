# Generated by Django 4.2.14 on 2024-08-17 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0014_alter_revisor_move_shops_alter_revisor_shops_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revisor',
            name='move_shops',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='revisor',
            name='shops',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='revisor',
            name='way_shops',
            field=models.IntegerField(default=0),
        ),
    ]