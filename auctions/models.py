from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils import timezone
import datetime


class User(AbstractUser):
    pass


class Theme(models.Model):
    """Category of LEGO."""

    theme_name = models.CharField(max_length=128, blank=False)

    def __str__(self):
        return self.theme_name


class Item(models.Model):
    """Characteristics of each set."""

    year_limit_mim = int(1943)
    year_limit_max = int(datetime.datetime.now().year) + 1

    item_id = models.IntegerField(primary_key=True)
    item_name = models.CharField(max_length=64)
    item_year = models.IntegerField(validators=[
        MinValueValidator(year_limit_mim), MaxValueValidator(year_limit_max)
        ])
    item_theme = models.ForeignKey(Theme, on_delete=models.PROTECT, null=True, related_name="item_theme")
    item_url_image = models.CharField(max_length=1000, blank=True)

    class Meta:
        """Unique subcategory inside one category."""

        unique_together = ("item_id", "item_name", "item_year", "item_theme")

    def __str__(self):
        return f"{self.item_id}: {self.item_name}"


class Condition(models.Model):
    """Condititon of each selling item (new/old etc.)."""

    item_condition = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.item_condition


class Listing(models.Model):
    title = models.ForeignKey(Item, on_delete=models.PROTECT, blank=False, related_name="lot_title")
    description = models.CharField(max_length=1000, blank=False)
    condition = models.ForeignKey(Condition, on_delete=models.PROTECT, blank=False, related_name="lot_condition")
    seller = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, related_name="lot_user")
    winner = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True, related_name="lot_winner")
    price = models.DecimalField(blank=False, max_digits=10, decimal_places=2)
    final_price = models.DecimalField(blank=False, max_digits=10, decimal_places=2, default=0)
    shipping = models.BooleanField(default=False)
    url_image = models.CharField(max_length=1000, blank=True)
    active_listing = models.BooleanField(default=True)
    watchlist = models.ManyToManyField(User, blank=True, null=True, related_name="watchlist_users")
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.title} / {self.seller}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=False, related_name="comment_user")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=False, related_name="comment_listing")
    review = models.CharField(max_length=300, blank=False)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} comments {self.listing}"


class Bid(models.Model):
    bid = models.DecimalField(blank=False, max_digits=10, decimal_places=2)
    bid_listing = models.ForeignKey(Listing, on_delete=models.CASCADE, blank=False, related_name="bid_listing")
    bid_user = models.ForeignKey(User, on_delete=models.PROTECT, blank=False, related_name="bid_user")
    date = models.DateTimeField(default=timezone.now)
