# Generated by Django 4.2.14 on 2024-08-18 00:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('counting', '0002_alter_worklog_id'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='worklog',
            unique_together=set(),
        ),
    ]