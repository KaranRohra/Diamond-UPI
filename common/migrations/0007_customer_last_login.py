# Generated by Django 3.1.7 on 2021-04-18 09:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0006_auto_20210411_1157'),
    ]

    operations = [
        migrations.AddField(
            model_name='customer',
            name='last_login',
            field=models.DateTimeField(blank=True, default=django.utils.timezone.now),
        ),
    ]
