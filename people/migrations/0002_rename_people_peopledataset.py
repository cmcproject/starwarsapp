# Generated by Django 4.0.4 on 2023-03-03 07:55

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("people", "0001_initial"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="People",
            new_name="PeopleDataset",
        ),
    ]
