# Generated by Django 3.0.1 on 2020-01-09 13:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_auto_20200108_1952'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Users',
            new_name='User',
        ),
    ]
