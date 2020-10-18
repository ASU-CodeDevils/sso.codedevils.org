# Generated by Django 2.0.1 on 2020-09-06 09:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_user_slack_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='tz_offset',
            field=models.IntegerField(blank=True, db_column='TzOffset', default=0, help_text='UTC offset in seconds', validators=[django.core.validators.MinValueValidator(-43200), django.core.validators.MaxValueValidator(54000)], verbose_name='UTC Offset'),
            preserve_default=False,
        ),
    ]
