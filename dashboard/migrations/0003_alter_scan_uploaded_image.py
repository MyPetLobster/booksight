# Generated by Django 5.0.4 on 2024-05-12 23:02

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0002_alter_scan_uploaded_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="scan",
            name="uploaded_image",
            field=models.ImageField(
                blank=True, default="", null=True, upload_to="uploaded_images/"
            ),
        ),
    ]
