"""
All models for core app are defined here.
"""
from django.conf import settings
from django_countries.fields import CountryField
from django.db import models
from django.shortcuts import reverse


class Actor(models.Model):
    """
    Actor model.
    """
    name = models.CharField(max_length=100)  # Name of the actor

    class Meta:
        ordering = ["name"]  # Order actors by name

    def __str__(self):
        return self.name


class Director(models.Model):
    """
    Director model.
    """
    name = models.CharField(max_length=100)  # Name of the director

    class Meta:
        ordering = ["name"]  # Order directors by name

    def __str__(self):
        return self.name


class Genre(models.Model):
    """
    Genre model.
    """
    name = models.CharField(max_length=100)  # Name of the genre

    class Meta:
        ordering = ["name"]  # Order genres by name

    def __str__(self):
        return self.name


class Movie(models.Model):
    """
    Movie model.
    """

    title = models.CharField(max_length=100)  # Title of the movie
    runtime = models.IntegerField(blank=True, null=True)  # Movie runtime
    year = models.IntegerField()  # Release year of the movie
    description = models.TextField(null=True)  # Basic movie description

    # IMDb rating for the movie
    rating = models.DecimalField(decimal_places=1, max_digits=2)
    genre = models.ManyToManyField(Genre)  # Movie genres, foreign key to Genre

    # Movie director, foreign key to Director
    directors = models.ManyToManyField(Director)

    # Movie actors, foreign key to Actor
    actors = models.ManyToManyField(Actor)
    certificate = models.TextField(max_length=4)  # Age rating for the movie
    icon_url = models.SlugField(max_length=220, null=True)
    poster_url = models.SlugField(max_length=220, null=True)
    big_poster_url = models.SlugField(max_length=220, null=True)

    class Meta:
        ordering = ["rating"]  # Order movies by rating

    def get_absolute_url(self):
        """
        Returns the url to access a particular instance of the model.
        """
        return reverse("core:movie", kwargs={
            "pk": self.pk
        })

    def get_add_to_cart_url(self):
        """
        Returns the url to add the movie to cart.
        """
        return reverse("core:add-to-cart", kwargs={
            "pk": self.pk
        })

    def get_remove_from_cart_url(self):
        """
        Returns the url to add the movie to cart.
        """
        return reverse("core:remove-from-cart", kwargs={
            "pk": self.pk
        })

    def get_add_to_wishlist_url(self):
        """
        Returns the url to add the movie to cart.
        """
        return reverse("core:add-to-wishlist", kwargs={
            "pk": self.pk
        })

    def get_remove_from_wishlist_url(self):
        """
        Returns the url to add the movie to cart.
        """
        return reverse("core:remove-from-wishlist", kwargs={
            "pk": self.pk
        })

    def __str__(self):
        return self.title


class OrderItem(models.Model):
    """
    Links the Movie model. When a Movie object is added to the cart it becomes an OrderItem object.
    """
    # User who added the movie to the cart
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    item = models.ForeignKey(Movie, on_delete=models.CASCADE)
    ordered = models.BooleanField(default=False)  # If the order is completed

    DURATION_CHOICES = [
        ("D", "One Day"),
        ("W", "One Week"),
        ("P", "Permanent"),
    ]
    duration = models.CharField(
        max_length=1,
        choices=DURATION_CHOICES,
        default="D"
    )

    price = models.DecimalField(  # Price of the movie
        max_digits=5,
        decimal_places=2,
        default=100.00,
    )

    def __str__(self):
        return f"{self.item.title} rented for {self.get_duration_display()}"

    def save(self, *args, **kwargs):
        """
        Overriding default save() function to set price dynamically.
        """
        if self.duration == "P":
            self.price = 300.00
        elif self.duration == "W":
            self.price = 200.00
        else:
            self.price = 100.00

        super().save(*args, **kwargs)


class Order(models.Model):
    """Stores all the movies in the cart. Can be thought of as the model for the User's cart."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )  # User who made the order

    items = models.ManyToManyField(OrderItem)  # Movies in the cart

    start_date = models.DateTimeField(
        auto_now_add=True
    )  # Date when the order was started

    ordered_date = models.DateTimeField()  # Date when the order was confirmed

    ordered = models.BooleanField(default=False)  # If the order is completed

    address = models.ForeignKey(
        "Address", on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return f"{self.id}: {self.start_date}"

    def get_total(self):
        """
        Returns the total price of the order.
        """
        total = 0
        for order_item in self.items.all():
            total += order_item.price
        return total


class Address(models.Model):
    """The address model."""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    address1 = models.CharField(max_length=100)
    address2 = models.CharField(max_length=100)
    country = CountryField(multiple=False)
    pincode = models.CharField(max_length=100)
    default = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.user.username


class WishlistItem(models.Model):
    """Add movies to wishlist"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE)
    item = models.ForeignKey(Movie, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.item.title}"


class Wishlist(models.Model):
    """Stores all movies in wishlist"""
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE
    )  # User who added to the wishlist

    items = models.ManyToManyField(WishlistItem)  # Movies in the wishlist
