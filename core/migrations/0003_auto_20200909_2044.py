# Generated by Django 3.1.1 on 2020-09-09 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0002_auto_20200909_2028"),
    ]

    operations = [
        migrations.AlterField(
            model_name="event",
            name="attendees",
            field=models.ManyToManyField(
                blank=True, related_name="attending_events", to="core.Profile"
            ),
        ),
    ]
