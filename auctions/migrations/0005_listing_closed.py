# Generated by Django 5.1.5 on 2025-02-16 09:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0004_rename_listings_listing"),
    ]

    operations = [
        migrations.AddField(
            model_name="listing",
            name="closed",
            field=models.BooleanField(default=False),
        ),
    ]
