# Generated by Django 4.2 on 2023-07-03 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mc_and_datasheet', '0013_file_file_session'),
    ]

    operations = [
        migrations.AlterField(
            model_name='file',
            name='file_session',
            field=models.CharField(max_length=50),
        ),
    ]
