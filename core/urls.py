"""
core URL Configuration
"""
from django.urls import path

from core.views import (AboutView, CartView, CheckoutView, HomeView,
                        MovieDetailView, WishlistView, add_to_cart,
                        add_to_wishlist, remove_from_cart,
                        remove_from_wishlist, ProfileView, HistoryView)

app_name = "core"

urlpatterns = [
    path("", HomeView.as_view(), name="home"),
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("cart/", CartView.as_view(), name="cart"),
    path("history/", HistoryView.as_view(), name="history"),
    path("wishlist/", WishlistView.as_view(), name="wishlist"),
    path("movie/<pk>/", MovieDetailView.as_view(), name="movie"),
    path("add-to-cart/<pk>/", add_to_cart, name="add-to-cart"),
    path("remove-from-cart/<pk>/", remove_from_cart, name="remove-from-cart"),
    path("add-to-wishlist/<pk>/", add_to_wishlist, name="add-to-wishlist"),
    path("remove-from-wishlist/<pk>/",
         remove_from_wishlist, name="remove-from-wishlist"),
    path("about/", AboutView.as_view(), name="about"),
    path("profile/", ProfileView.as_view(), name="profile"),
]
