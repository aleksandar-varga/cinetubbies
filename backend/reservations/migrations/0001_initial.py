# Generated by Django 2.0.4 on 2018-05-02 07:46

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RewardScale',
            fields=[
                ('status', models.CharField(choices=[('basic', 'Basic'), ('bronze', 'Bronze'), ('silver', 'Silver'), ('gold', 'Gold')], max_length=6, primary_key=True, serialize=False)),
                ('min_points', models.PositiveSmallIntegerField()),
                ('max_points', models.PositiveSmallIntegerField()),
            ],
        ),
    ]
