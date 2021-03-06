# Generated by Django 2.0.1 on 2020-08-20 03:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20200820_0253'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='slack_id',
            field=models.CharField(blank=True, db_column='SlackId', help_text='ID assigned to this user on Slack', max_length=12, null=True),
        ),
    ]
