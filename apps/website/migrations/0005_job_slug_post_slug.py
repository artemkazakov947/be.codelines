# Generated by Django 4.2.2 on 2023-07-10 14:14

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("website", "0004_alter_post_title"),
    ]

    operations = [
        migrations.AddField(
            model_name="job",
            name="slug",
            field=models.SlugField(default="slug"),
        ),
        migrations.AddField(
            model_name="post",
            name="slug",
            field=models.SlugField(default="slug"),
        ),
    ]
