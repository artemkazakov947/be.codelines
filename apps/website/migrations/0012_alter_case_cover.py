# Generated by Django 4.2.2 on 2023-07-14 09:48

import apps.website.models
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0011_case"),
    ]

    operations = [
        migrations.AlterField(
            model_name="case",
            name="cover",
            field=models.ImageField(upload_to=apps.website.models.case_file_path),
        ),
    ]
