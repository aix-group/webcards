# Generated by Django 4.0.4 on 2023-01-22 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mc_and_datasheet', '0002_item_mc_section_delete_answer_delete_question_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='item',
            old_name='todolist',
            new_name='mc_section',
        ),
    ]
