# Generated by Django 4.2 on 2023-05-08 12:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('comments', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='comment',
            old_name='content',
            new_name='body',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='edited',
            new_name='is_edited',
        ),
        migrations.RenameField(
            model_name='comment',
            old_name='pinned',
            new_name='is_pinned',
        ),
    ]
