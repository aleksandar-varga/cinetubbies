# Generated by Django 2.0.4 on 2018-05-05 13:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('theaters', '0005_auto_20180427_1617'),
        ('sale_tickets', '0002_auto_20180505_1331'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticketonsale',
            name='theater',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, related_name='tickets_on_sale', to='theaters.Theater'),
            preserve_default=False,
        ),
    ]
