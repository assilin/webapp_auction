from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
# from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.utils.datastructures import MultiValueDictKeyError

from .models import Bid, Comment, Condition, Item, Listing, Theme, User


def index(request):
    all_listing = Listing.objects.filter(active_listing=True).order_by("-date")
    all_theme = Theme.objects.all()

    return render(request, "auctions/index.html", {
        "themes": all_theme,
        "listings": all_listing,
    })


def my_listings(request):
    current_user = request.user
    my_listing = Listing.objects.filter(seller=current_user)
    all_theme = Theme.objects.all()

    return render(request, "auctions/index.html", {
        "themes": all_theme,
        "listings": my_listing,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required
def new_listing(request):
    if request.method == "POST":
        try:
            # page 2 - get data from the form
            listing_id = request.POST["itemId"]
            listing_description = request.POST["itemDiscription"]
            listing_condition = request.POST["itemCondition"]
            listing_price = request.POST["itemPrice"]
            listing_shipping = True if request.POST.get("itemShipping", False) == 1 else False
            listing_url = request.POST["itemImage"]

            listing_seller = request.user


            # get data from the base
            listing_condition_data = Condition.objects.get(item_condition=listing_condition)
            listing_id_data = Item.objects.get(item_id=listing_id)

            # create new object and save it
            new_listing = Listing(
                title=listing_id_data,
                description=listing_description,
                condition=listing_condition_data,
                seller=listing_seller,
                price=listing_price,
                shipping=listing_shipping,
                url_image=listing_url,
            )
            new_listing.save()
            return HttpResponseRedirect(reverse("index"))

        except MultiValueDictKeyError:
            # page 1 - choose the set
            try:
                title = request.POST["itemObject"]
                item_id = title.split(":")[0]
                item_object = Item.objects.get(pk=item_id)

                return render(request, "auctions/new_listing.html", {
                    "item": item_object,
                    "conditions": Condition.objects.all(),
                })
            except ValueError:
                return render(request, "auctions/new_listing.html", {
                    "items": Item.objects.all(),
                })

    else:
        # GET method
        return render(request, "auctions/new_listing.html", {
            "items": Item.objects.all(),
        })


def listing(request, id):
    current_listing = Listing.objects.get(pk=id)
    current_user = request.user
    is_in_watchlist = current_user in current_listing.watchlist.all()
    is_owner = current_listing.seller == current_user
    is_winner = current_listing.winner == current_user
    comments = Comment.objects.filter(listing_id=id).order_by("-date")
    bids = Bid.objects.filter(bid_listing=current_listing).order_by("-date")

    return render(request, "auctions/listing.html", {
        "listing": Listing.objects.get(pk=id),
        "watchlist": is_in_watchlist,
        "comments": comments,
        "bids": bids,
        "is_owner": is_owner,
        "is_winner": is_winner,
    })


@login_required
def close_listing(request, id):
    current_listing = Listing.objects.get(pk=id)
    current_user = request.user
    # double check
    is_owner = current_listing.seller == current_user

    if is_owner:
        is_in_watchlist = current_user in current_listing.watchlist.all()
        comments = Comment.objects.filter(listing_id=id).order_by("-date")
        bids = Bid.objects.filter(bid_listing=current_listing).order_by("-date")

        try:
            last_bid = bids.first().bid
            last_bid_user = bids.first().bid_user
        except AttributeError:
            last_bid = 0
            last_bid_user = None

        current_listing.active_listing = False
        current_listing.final_price = last_bid
        current_listing.winner = last_bid_user
        current_listing.save()
        is_winner = current_listing.winner == current_user
        return render(request, "auctions/listing.html", {
            "listing": Listing.objects.get(pk=id),
            "watchlist": is_in_watchlist,
            "comments": comments,
            "bids": bids,
            "is_owner": is_owner,
            "is_winner": is_winner,
        })
    else:
        return HttpResponseRedirect(reverse("listing", args=(id, )))


def filter_category(request):
    if request.method == "POST":
        all_theme = Theme.objects.all()
        theme = request.POST["itemTheme"]
        theme_data = Theme.objects.get(theme_name=theme)

        theme_listing = Listing.objects.filter(title__item_theme__theme_name=theme_data, active_listing=True).order_by("-date")

        return render(request, "auctions/index.html", {
            "themes": all_theme,
            "listings": theme_listing,
        })


@login_required
def add_to_watchlist(request, id):
    current_user = request.user
    current_listing = Listing.objects.get(pk=id)
    current_listing.watchlist.add(current_user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))


@login_required
def remove_from_watchlist(request, id):
    current_user = request.user
    current_listing = Listing.objects.get(pk=id)
    current_listing.watchlist.remove(current_user)
    return HttpResponseRedirect(reverse("listing", args=(id, )))


@login_required
def watchlist(request):
    current_user = request.user
    user_listing = current_user.watchlist_users.all()
    return render(request, 'auctions/watchlist.html', {
        "listings": user_listing,
    })


@login_required
def add_comment(request, id):
    current_user = request.user
    current_listing = Listing.objects.get(pk=id)
    comment = request.POST["usersComment"]

    # create new comment and save it
    new_comment = Comment(
        user=current_user,
        listing=current_listing,
        review=comment,
    )
    new_comment.save()

    return HttpResponseRedirect(reverse("listing", args=(id, )))


@login_required
def place_bid(request, id):
    if request.method == "POST":
        current_user = request.user
        current_listing = Listing.objects.get(pk=id)
        current_bid = float(request.POST["itemBid"])
        is_in_watchlist = current_user in current_listing.watchlist.all()
        comments = Comment.objects.filter(listing_id=id).order_by("-date")

        start_price = Listing.objects.get(pk=id).price

        try:
            last_bid = Bid.objects.filter(bid_listing=current_listing).order_by("-date").first().bid
        except AttributeError:
            last_bid = 0

        if current_bid <= start_price or current_bid <= last_bid:
            bids = Bid.objects.filter(bid_listing=current_listing).order_by("-date")
            message = "Your bid should be large than the last bid or starting price"
            return render(request, "auctions/listing.html", {
                "listing": Listing.objects.get(pk=id),
                "watchlist": is_in_watchlist,
                "comments": comments,
                "message": message,
                "bids": bids,
            })
        else:
            new_bid = Bid(
                bid=current_bid,
                bid_listing=current_listing,
                bid_user=current_user,
            )
            new_bid.save()
            bids = Bid.objects.filter(bid_listing=current_listing).order_by("-date")
            message = "Well done!"
            return render(request, "auctions/listing.html", {
                "listing": Listing.objects.get(pk=id),
                "watchlist": is_in_watchlist,
                "comments": comments,
                "message": message,
                "bids": bids,
            })