# Generated by Django 2.0.4 on 2018-04-27 14:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0008_auto_20180427_1117'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('cinema_admin', 'Theater Admin'), ('fan_zone_admin', 'Fan Zone Admin'), ('user', 'User')], default='user', max_length=20),
        ),
    ]
