# Generated by Django 4.0.4 on 2022-12-22 11:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_articlecomment'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ArticleRate',
        ),
    ]