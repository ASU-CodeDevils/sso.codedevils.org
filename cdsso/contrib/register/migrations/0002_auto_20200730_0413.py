# Generated by Django 2.0.1 on 2020-07-30 04:13

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ("register", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="studentregistration",
            options={
                "get_latest_by": "-date_registered",
                "ordering": (
                    "-slack_registered",
                    "-sds_registered",
                    "-date_registered",
                ),
                "verbose_name": "Student Registration",
                "verbose_name_plural": "Student Registration",
            },
        ),
        migrations.AddField(
            model_name="studentregistration",
            name="date_registered",
            field=models.DateTimeField(
                auto_now_add=True,
                db_column="DateRegistered",
                default=django.utils.timezone.now,
                help_text="The date/time the student submitted their registration form",
                verbose_name="Date Registered",
            ),
            preserve_default=False,
        ),
    ]
