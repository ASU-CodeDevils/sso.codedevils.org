# Generated by Django 2.0.1 on 2020-09-06 09:35

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('register', '0004_auto_20200906_0923'),
    ]

    operations = [
        migrations.AlterField(
            model_name='knownmember',
            name='tz_offset',
            field=models.IntegerField(blank=True, db_column='TzOffset', default=0, help_text='UTC offset in seconds', null=True, validators=[django.core.validators.MinValueValidator(-43200), django.core.validators.MaxValueValidator(54000)], verbose_name='UTC Offset'),
        ),
    ]
