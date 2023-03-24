from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("add_comment/<int:id>", views.add_comment, name="add_comment"),
    path("add_to_watchlist/<int:id>", views.add_to_watchlist, name="add_to_watchlist"),
    path("close_listing/<int:id>", views.close_listing, name="close_listing"),
    path("filter_category", views.filter_category, name="filter_category"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("my_listings", views.my_listings, name="my_listings"),
    path("new_listing", views.new_listing, name="new_listing"),
    path("place_bid/<int:id>", views.place_bid, name="place_bid"),
    path("register", views.register, name="register"),
    path("remove_from_watchlist/<int:id>", views.remove_from_watchlist, name="remove_from_watchlist"),
    path("watchlist", views.watchlist, name="watchlist"),
]
