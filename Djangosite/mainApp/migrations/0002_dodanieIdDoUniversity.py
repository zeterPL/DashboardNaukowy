# Generated by Django 4.1.9 on 2023-05-14 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("mainApp", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="university",
            name="id",
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]
