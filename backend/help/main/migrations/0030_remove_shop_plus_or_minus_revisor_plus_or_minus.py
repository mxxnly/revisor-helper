# Generated by Django 4.2.14 on 2024-08-29 18:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0029_alter_shop_plus_or_minus'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='shop',
            name='plus_or_minus',
        ),
        migrations.AddField(
            model_name='revisor',
            name='plus_or_minus',
            field=models.IntegerField(blank=True, default=0, null=True),
        ),
    ]
