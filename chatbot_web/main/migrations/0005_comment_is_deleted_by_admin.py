# Generated by Django 5.2.4 on 2025-07-11 01:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0004_comment"),
    ]

    operations = [
        migrations.AddField(
            model_name="comment",
            name="is_deleted_by_admin",
            field=models.BooleanField(default=False),
        ),
    ]
