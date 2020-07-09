# Generated by Django 2.0.1 on 2020-07-06 12:29

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentRegistration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slack_registered', models.BooleanField(db_column='SlackRegistered', default=False, help_text='The user has been registered on Slack', verbose_name='Registered on Slack')),
                ('sds_registered', models.BooleanField(db_column='SDSRegistered', default=False, help_text='The user has been registered on SunDevilSync. This is True by default for alumni.', verbose_name='Registered on SunDevilSync')),
                ('user', models.OneToOneField(db_column='UserId', help_text="This user's progress in the registration process.", on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
            options={
                'verbose_name': 'Student Registration',
                'verbose_name_plural': 'Student Registration',
            },
        ),
    ]
