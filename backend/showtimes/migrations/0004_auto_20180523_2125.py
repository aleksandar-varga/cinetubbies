# Generated by Django 2.0.4 on 2018-05-23 21:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('showtimes', '0003_auto_20180513_1938'),
    ]

    operations = [
        migrations.AlterField(
            model_name='showtime',
            name='auditorium',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='showtimes', to='theaters.Auditorium'),
        ),
    ]
