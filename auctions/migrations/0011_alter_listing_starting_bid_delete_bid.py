# Generated by Django 5.1.5 on 2025-03-09 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("auctions", "0010_remove_bid_auction_remove_bid_bid_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="listing",
            name="starting_bid",
            field=models.DecimalField(decimal_places=2, default="0", max_digits=10),
        ),
        migrations.DeleteModel(
            name="Bid",
        ),
    ]
