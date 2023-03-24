# Generated by Django 4.1.7 on 2023-03-15 22:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0012_alter_comment_listing'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bid',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid', models.FloatField()),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('bid_listing', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bid_listing', to='auctions.listing')),
                ('bid_user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='bid_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]