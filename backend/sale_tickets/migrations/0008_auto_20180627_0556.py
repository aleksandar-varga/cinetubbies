# Generated by Django 2.0.5 on 2018-06-27 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sale_tickets', '0007_ticketonsale_deleted'),
    ]

    operations = [
        migrations.AddField(
            model_name='booking',
            name='version',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='booking',
            name='seat',
            field=models.IntegerField(default=0),
        ),
    ]
