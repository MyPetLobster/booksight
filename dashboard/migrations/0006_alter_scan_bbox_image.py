# Generated by Django 5.0.4 on 2024-05-20 07:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0005_alter_scan_scan_status"),
    ]

    operations = [
        migrations.AlterField(
            model_name="scan",
            name="bbox_image",
            field=models.URLField(blank=True, default="", null=True),
        ),
    ]