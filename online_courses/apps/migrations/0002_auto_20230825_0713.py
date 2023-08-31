# Generated by Django 3.2.16 on 2023-08-25 07:13

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('apps', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='accountconfirmation',
            name='expiry_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 25, 11, 13, 26, 733653, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='start_time',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 25, 11, 13, 26, 684964, tzinfo=utc)),
        ),
        migrations.AlterField(
            model_name='meeting',
            name='uuid',
            field=models.CharField(max_length=40),
        ),
    ]