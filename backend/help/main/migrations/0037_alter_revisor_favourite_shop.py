# Generated by Django 4.2.14 on 2024-09-17 18:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0036_revisor_date_of_birth_revisor_favourite_shop'),
    ]

    operations = [
        migrations.AlterField(
            model_name='revisor',
            name='favourite_shop',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='fav_shop', to='main.shop'),
        ),
    ]