# Generated by Django 4.1.7 on 2023-03-12 18:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_item_item_url_image'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='theme',
            unique_together=set(),
        ),
        migrations.RemoveField(
            model_name='theme',
            name='category_choice',
        ),
        migrations.DeleteModel(
            name='Category',
        ),
    ]