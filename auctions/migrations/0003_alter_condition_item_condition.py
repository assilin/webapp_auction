# Generated by Django 4.1.7 on 2023-03-10 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_item_item_category_item_item_theme_listing_year_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='condition',
            name='item_condition',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
