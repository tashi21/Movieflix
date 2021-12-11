"""
All views for core app are defined here.
"""
from django.contrib.auth.password_validation import validate_password
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone
from django.views.generic import DetailView, ListView, TemplateView, View

from core.forms import CheckoutForm, PasswordForm, ProfileForm, Search
from core.models import (Address, Movie, Order, OrderItem, Profile, Wishlist,
                         WishlistItem)


class HistoryView(LoginRequiredMixin, ListView):
    """The past orders View"""
    queryset = Order.objects.filter(ordered=True)
    context_object_name = "orders"
    template_name = "orders.html"
    paginate_by = 1


class ProfileView(LoginRequiredMixin, TemplateView):
    """
    Profile view.
    """
    template_name = "profile.html"

    def get(self, *args, **kwargs):
        """Get profile view."""
        profile_form = ProfileForm()
        password_form = PasswordForm()
        profile = Profile.objects.get(user=self.request.user)
        return render(self.request, "profile.html", {"profile_form": profile_form, "password_form": password_form, "user": self.request.user, "profile": profile})

    def post(self, *args, **kwargs):
        """Update profile view."""
        profile_form = ProfileForm(
            self.request.POST or None, self.request.FILES)
        password_form = PasswordForm(self.request.POST or None)
        user = self.request.user
        profile = Profile.objects.get(user=user)
        if profile_form.is_valid():
            print(profile_form.cleaned_data)
            user.first_name = profile_form.cleaned_data["first_name"]
            user.last_name = profile_form.cleaned_data["last_name"]
            try:
                testuser = get_user_model().objects.get(
                    username=profile_form.cleaned_data["username"])
                if testuser != user:
                    messages.warning(self.request, "Username already exists")
                    return redirect("core:profile")
            except ObjectDoesNotExist:
                user.username = profile_form.cleaned_data["username"]
            try:
                testuser = get_user_model().objects.get(
                    username=profile_form.cleaned_data["email"])
                if testuser != user:
                    messages.warning(self.request, "Email already exists")
                    return redirect("core:profile")
            except ObjectDoesNotExist:
                user.email = profile_form.cleaned_data["email"]
            profile.phone_number = profile_form.cleaned_data["phone_number"]
            if profile_form.cleaned_data["profile_pic"]:
                profile.profile_pic = profile_form.cleaned_data["profile_pic"]
            user.save()
            profile.save()
            messages.success(self.request, "Profile updated successfully")

        if password_form.is_valid():
            if password_form.cleaned_data["password1"] == "" and password_form.cleaned_data["password2"] == "" and password_form.cleaned_data["password_old"] == "":
                return redirect("core:profile")
            old_password = password_form.cleaned_data["password_old"]
            correct = user.check_password(old_password)
            if correct:
                try:
                    validate_password(
                        password_form.cleaned_data["password1"])
                except ValidationError:
                    messages.warning(
                        self.request, "Password does not pas validation checks.")
                    return redirect("core:profile")
                else:
                    if password_form.cleaned_data["password1"] == password_form.cleaned_data["password2"]:
                        user.set_password(
                            password_form.cleaned_data["password1"])
                        user.save()
                        messages.success(
                            self.request, "Password updated successfully!")
                    else:
                        messages.warning(
                            self.request, "Passwords do not match.")
                        return redirect("core:profile")
            else:
                messages.warning(self.request, "Old password is incorrect.")
        return redirect("core:profile")


class CheckoutView(LoginRequiredMixin, View):
    """The Checkout View"""

    def get(self, *args, **kwargs):
        """Get the checkout view"""
        form = CheckoutForm()
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {"form": form, "order": order}
            address_qs = Address.objects.filter(
                user=self.request.user,
                default=True,
            )
            if address_qs.exists():
                context.update({"default_address": address_qs[0]})

            return render(self.request, "checkout.html", context)
        except ObjectDoesNotExist:
            messages.info(self.request, "You do not have any current orders.")
            return redirect("core:home")

    def post(self, *args, **kwargs):
        """Post the checkout view"""
        form = CheckoutForm(self.request.POST or None)
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            if form.is_valid():
                use_default = form.cleaned_data.get("use_default")
                if use_default:
                    address_qs = Address.objects.filter(
                        user=self.request.user,
                        default=True,
                    )
                    if address_qs.exists():
                        address = address_qs[0]

                    else:
                        messages.info(
                            self.request, "No default address available")
                        return redirect("core:checkout")
                else:
                    address1 = form.cleaned_data.get("address1")
                    address2 = form.cleaned_data.get("address2")
                    country = form.cleaned_data.get("country")
                    pincode = form.cleaned_data.get("pincode")
                    payment_option = form.cleaned_data.get("payment_option")
                    address = Address(
                        user=self.request.user,
                        address1=address1,
                        address2=address2,
                        country=country,
                        pincode=pincode,
                    )
                address.save()
                order.address = address
                ordered_items = order.items.all()
                ordered_items.update(ordered=True)
                for item in ordered_items:
                    item.save()
                order.ordered = True
                order.save()
                set_default = form.cleaned_data.get("set_default")
                if set_default:
                    address.default = True
                    address.save()
                messages.success(
                    self.request, "Your order was successful! We look forward to seeing you more.")
                return redirect("core:home")
            messages.warning(
                self.request, "Checkout failed, please try again. Sorry for the inconvenience.")
            return redirect("core:checkout")

        except ObjectDoesNotExist:
            messages.error(self.request, "You do not have any current orders.")
            return redirect("core:cart")


class AboutView(TemplateView):
    """The About Page"""
    template_name = "about.html"


class CartView(LoginRequiredMixin, View):
    """The Cart View"""

    def get(self, *args, **kwargs):
        """Get the cart view"""
        try:
            order = Order.objects.get(user=self.request.user, ordered=False)
            context = {"order": order, }
            return render(self.request, "cart.html", context)
        except ObjectDoesNotExist:
            return render(self.request, "cart.html")


class WishlistView(LoginRequiredMixin, View):
    """The Wishlist View"""

    def get(self, *args, **kwargs):
        """Get the wishlist view"""
        try:
            wishlist = Wishlist.objects.get(user=self.request.user)
            context = {"wishlist": wishlist}
            return render(self.request, "wishlist.html", context)
        except ObjectDoesNotExist:
            return render(self.request, "wishlist.html")


class HomeView(ListView):
    """
    View for home page. Lists all the movies in the database.
    """
    model = Movie
    context_object_name = "movies"
    paginate_by = 15
    template_name = "home.html"

    def get_filter_args(self):
        """
        Get the filter arguments from the request.
        """
        filter_args = {}
        filter_args["directors__name__contains"] = self.request.GET.get(
            "director")
        filter_args["actors__name__contains"] = self.request.GET.get("actor")
        filter_args["genre__name__contains"] = self.request.GET.get("genre")
        filter_args = {
            key: value for key, value in filter_args.items() if value}
        return filter_args

    def get_queryset(self):
        filter_args = self.get_filter_args()
        queryset = super().get_queryset().filter(**filter_args).distinct()
        return queryset

    def get_context_data(self, **kwargs):
        """
        Create the context dictionary.
        """
        context = super().get_context_data(**kwargs)
        context["form"] = Search()
        return context


class MovieDetailView(DetailView):
    """The movie detail view. Displays details of one movie."""
    model = Movie
    template_name = "movie.html"

    def get_context_data(self, **kwargs):
        """
        Create the context dictionary.
        """
        context = super().get_context_data(**kwargs)
        try:
            order_items = OrderItem.objects.filter(
                user=self.request.user, item=self.object, ordered=False)
            if order_items.exists():
                order_item = order_items[0]
                context.update({"order_item": order_item})
            wishlist_items = WishlistItem.objects.filter(
                user=self.request.user, item=self.object)
            if wishlist_items.exists():
                wishlist_item = wishlist_items[0]
                context.update({"wishlist_item": wishlist_item})
            return context
        except:
            return context


@ login_required()
def add_to_cart(request, pk):
    """
    Add a movie to cart.
    """
    movie = get_object_or_404(Movie, pk=pk)
    order_item, created = OrderItem.objects.get_or_create(  # Get the order item or create a new one
        item=movie,
        user=request.user,
        ordered=False
    )
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    # Get the duration of the movie from the form
    duration = request.POST.get("duration")
    if duration != order_item.duration:
        order_item.duration = duration
        messages.info(
            request, f"The rental duration of {movie.title} has been updated!"
        )
    order_item.save()  # Save the updated duration

    if order_qs.exists():  # If the user has an active order
        order = order_qs[0]  # Get the order
        # If the item is in the order
        if order.items.filter(item__pk=movie.pk).exists():
            # If the duration is different from the one in the order
            if duration != order.items.filter(item__pk=movie.pk)[0].duration:
                order.items.filter(item__pk=movie.pk).update(
                    duration=duration)  # Update the duration in the order

        else:
            order.items.add(order_item)  # Add the item to the order
            messages.info(
                request, f"{movie.title} has been added to your cart!"
            )

    else:  # If the user does not have an active order
        ordered_date = timezone.now()  # Get the current date
        order = Order.objects.create(  # Create a new order
            user=request.user,
            ordered_date=ordered_date
        )
        order.items.add(order_item)  # Add the item to the order
        messages.info(
            request, f"{movie.title} has been added to your cart!"
        )

    return redirect("core:movie", pk=pk)


@ login_required()
def remove_from_cart(request, pk):
    """Remove a movie from cart."""
    movie = get_object_or_404(Movie, pk=pk)
    order_qs = Order.objects.filter(user=request.user, ordered=False)

    if order_qs.exists():  # If the user has an active order
        order = order_qs[0]  # Get the order
        # If the item is in the order
        if order.items.filter(item__pk=movie.pk).exists():
            order_item = OrderItem.objects.filter(  # Get the order item
                item=movie,
                user=request.user,
                ordered=False
            )[0]

            order.items.remove(order_item)  # Remove the item from the order
            order_item.delete()  # Delete the order item
            messages.info(
                request, f"{movie.title} has been removed from your cart :("
            )

    # Redirect to the previous page
    return redirect(request.META["HTTP_REFERER"])


@ login_required()
def add_to_wishlist(request, pk):
    """Add a movie to wishlist."""
    movie = get_object_or_404(Movie, pk=pk)
    wishlist_item, created = WishlistItem.objects.get_or_create(  # Get the wishlist item or create a new one
        item=movie,
        user=request.user
    )
    wishlist_qs = Wishlist.objects.filter(user=request.user)

    if wishlist_qs.exists():  # If the user has an active wishlist
        wishlist = wishlist_qs[0]  # Get the wishlist
        # If the item is not in the wishlist
        if not wishlist.items.filter(item__pk=movie.pk).exists():
            wishlist.items.add(wishlist_item)  # Add the item to the wishlist
            messages.info(
                request, f"{movie.title} has been added to your Wishlist!"
            )

    else:  # If the user does not have an active wishlist
        wishlist = Wishlist.objects.create(  # Create a new wishlist
            user=request.user
        )
        wishlist.items.add(wishlist_item)  # Add the item to the wishlist
        messages.info(
            request, f"{movie.title} has been added to your Wishlist!"
        )

    # Redirect to the previous page
    return redirect(request.META["HTTP_REFERER"])


@ login_required()
def remove_from_wishlist(request, pk):
    """Remove a movie from wishlist."""
    movie = get_object_or_404(Movie, pk=pk)
    wishlist_qs = Wishlist.objects.filter(user=request.user)

    if wishlist_qs.exists():  # If the user has an active wishlist
        wishlist = wishlist_qs[0]  # Get the wishlist
        # If the item is in the wishlist
        if wishlist.items.filter(item__pk=movie.pk).exists():
            wishlist_item = WishlistItem.objects.filter(  # Get the wishlist item
                item=movie,
                user=request.user,
            )[0]

            # Remove the item from the wishlist
            wishlist.items.remove(wishlist_item)
            wishlist_item.delete()  # Delete the wishlist item
            messages.info(
                request, f"{movie.title} has been removed from your Wishlist :("
            )

    # Redirect to the previous page
    return redirect(request.META["HTTP_REFERER"])
