"""
Register models in admin database.
"""
from django.contrib import admin

from core.models import (
    Actor, Address, Director, Genre, Movie, Order, OrderItem, Wishlist, WishlistItem
)

# Register your models here.
admin.site.register(Actor)
admin.site.register(Address)
admin.site.register(Director)
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Wishlist)
admin.site.register(WishlistItem)
