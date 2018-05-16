# Generated by Django 2.0.5 on 2018-05-15 06:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('fan_zone', '0005_prop_version'),
    ]

    operations = [
        migrations.CreateModel(
            name='Reservation',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('quantity', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.AlterModelManagers(
            name='prop',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='prop',
            name='quantity',
            field=models.PositiveSmallIntegerField(null=True),
        ),
        migrations.AddField(
            model_name='reservation',
            name='prop',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='+', to='fan_zone.Prop'),
        ),
        migrations.AddField(
            model_name='reservation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='prop_reservations', to=settings.AUTH_USER_MODEL),
        ),
    ]
