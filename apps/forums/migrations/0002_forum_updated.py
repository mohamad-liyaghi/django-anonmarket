# Generated by Django 4.2 on 2023-05-12 16:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forums', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='forum',
            name='updated',
            field=models.BooleanField(default=False),
        ),
    ]