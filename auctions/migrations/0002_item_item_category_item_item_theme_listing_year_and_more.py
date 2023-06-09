# Generated by Django 4.1.7 on 2023-03-10 18:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='item_category',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='item_characteristic', to='auctions.category'),
        ),
        migrations.AddField(
            model_name='item',
            name='item_theme',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='item_characteristic', to='auctions.theme'),
        ),
        migrations.AddField(
            model_name='listing',
            name='year',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, related_name='year', to='auctions.item'),
        ),
        migrations.AlterField(
            model_name='category',
            name='category_name',
            field=models.CharField(max_length=64, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='item',
            unique_together={('item_id', 'item_name', 'item_year', 'item_theme', 'item_category')},
        ),
    ]
