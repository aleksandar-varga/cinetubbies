# Generated by Django 2.0.4 on 2018-04-29 12:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_movie_theater'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='movie',
            name='admin',
        ),
    ]
