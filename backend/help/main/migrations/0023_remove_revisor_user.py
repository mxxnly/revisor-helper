# Generated by Django 4.2.14 on 2024-08-21 20:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0022_alter_revisor_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='revisor',
            name='user',
        ),
    ]