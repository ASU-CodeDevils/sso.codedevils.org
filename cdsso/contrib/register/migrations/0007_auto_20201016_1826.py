# Generated by Django 2.0.1 on 2020-10-16 18:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("register", "0006_auto_20201003_0848"),
    ]

    operations = [
        migrations.AddField(
            model_name="studentregistration",
            name="completed_registration_notification",
            field=models.BooleanField(
                db_column="CompletedRegistrationNotification",
                default=False,
                help_text="Flag to track if this user has been notified that their registration has been completed.",
                verbose_name="Completed Registration Notification",
            ),
        ),
        migrations.AddField(
            model_name="studentregistration",
            name="sds_notified",
            field=models.BooleanField(
                db_column="SdsNotified",
                default=False,
                help_text="Flag to track whether a CodeDevils officer has been notified that this student needs to be added to SunDevilSync",
                verbose_name="SunDevilSync Notification",
            ),
        ),
        migrations.AddField(
            model_name="studentregistration",
            name="slack_add_attempt",
            field=models.BooleanField(
                db_column="SlackAddAttempt",
                default=False,
                help_text="Flag to track if the API was used previously to add this user to Slack. This stops consecutive attempts of adding this user.",
                verbose_name="Slack Add Attempt",
            ),
        ),
    ]
