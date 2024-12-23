# Generated by Django 4.2.17 on 2024-12-24 02:56

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="RichPerson",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("rank", models.IntegerField()),
                ("name", models.CharField(max_length=255)),
                ("total_net_worth", models.CharField(max_length=50)),
                ("last_change", models.CharField(max_length=50)),
                ("ytd_change", models.CharField(max_length=50)),
                ("country_region", models.CharField(max_length=100)),
                ("industry", models.CharField(max_length=100)),
            ],
        ),
    ]
