# Generated by Django 4.2.2 on 2023-08-26 12:55

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_alter_token_access_expiration_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='token',
            name='access_expiration',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 26, 13, 45, 15, 7344, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='token',
            name='refresh_expiration',
            field=models.DateTimeField(default=datetime.datetime(2023, 8, 29, 12, 55, 15, 7344, tzinfo=datetime.timezone.utc)),
        ),
    ]
