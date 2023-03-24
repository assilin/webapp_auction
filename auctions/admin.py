from django.contrib import admin
from .models import Bid, Comment, Condition, Item, Listing, Theme, User


# Register your models here.


class BidAdmin(admin.ModelAdmin):
    list_display = ("bid_listing", "bid_user", "bid")
    list_filter = ("bid_listing", "bid_user", "bid",)
    ordering = ("bid_listing", "bid_user", "date",)


class ItemAdmin(admin.ModelAdmin):
    list_display = ("item_id", "item_year", "item_name", "item_theme")
    list_filter = ("item_theme",)
    search_fields = ("item_id", "item_name",)
    ordering = ("item_id", "item_year", "item_name",)


class ListingAdmin(admin.ModelAdmin):
    list_display = ("title", "seller", "price", "winner", "final_price", "active_listing", "id")
    list_filter = ("seller", "title", "condition",)
    search_fields = ("seller", "title", "condition",)


class ThemeAdmin(admin.ModelAdmin):
    list_display = ("id", "theme_name")


admin.site.register(Bid, BidAdmin)
admin.site.register(Comment)
admin.site.register(Condition)
admin.site.register(Item, ItemAdmin)
admin.site.register(Listing, ListingAdmin)
admin.site.register(Theme, ThemeAdmin)
admin.site.register(User)
