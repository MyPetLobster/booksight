# Generated by Django 5.0.4 on 2024-05-11 00:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Scan",
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
                ("uploaded_image", models.ImageField(upload_to="uploaded_images/")),
                ("object_creation_date", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "ordering": ["-object_creation_date"],
            },
        ),
        migrations.CreateModel(
            name="Spine",
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
                ("image_path", models.CharField(max_length=200)),
                ("avg_color", models.CharField(max_length=200)),
                ("dominant_color", models.CharField(max_length=200)),
                ("color_palette", models.CharField(max_length=200)),
                ("height", models.FloatField()),
                ("width", models.FloatField()),
                ("text", models.TextField()),
                ("title", models.CharField(max_length=200)),
                ("author", models.CharField(max_length=200)),
                ("possible_matches", models.TextField()),
                (
                    "scan",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="spines",
                        to="dashboard.scan",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Book",
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
                ("title", models.CharField(max_length=200)),
                ("subtitle", models.CharField(max_length=200)),
                ("authors", models.CharField(max_length=200)),
                ("language", models.CharField(max_length=200)),
                ("publisher", models.CharField(max_length=200)),
                ("date_published", models.DateField()),
                ("description", models.TextField()),
                ("isbn", models.CharField(max_length=200)),
                ("isbn10", models.CharField(max_length=200)),
                ("isbn13", models.CharField(max_length=200)),
                ("pages", models.IntegerField()),
                ("binding", models.CharField(max_length=200)),
                ("image_path", models.CharField(max_length=200)),
                ("confidence", models.FloatField()),
                (
                    "spine",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="books",
                        to="dashboard.spine",
                    ),
                ),
            ],
        ),
    ]
