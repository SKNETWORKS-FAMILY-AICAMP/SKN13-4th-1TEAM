# Generated by Django 5.2.4 on 2025-07-11 01:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0005_comment_is_deleted_by_admin"),
    ]

    operations = [
        migrations.AddField(
            model_name="post",
            name="is_announcement",
            field=models.BooleanField(default=False),
        ),
    ]
