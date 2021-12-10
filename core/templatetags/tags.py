"""Register custom tags"""

from core.models import Order, Wishlist
from django import template

register = template.Library()


@register.filter
def cart_item_count(user):
    """Returns number of items in user's cart"""
    if user.is_authenticated:
        qs = Order.objects.filter(user=user, ordered=False)
        if qs.exists():
            return qs[0].items.count()
    return 0


@register.filter
def wishlist_item_count(user):
    """Returns number of items in user's wishlist"""
    if user.is_authenticated:
        qs = Wishlist.objects.filter(user=user)
        if qs.exists():
            return qs[0].items.count()
    return 0


@register.simple_tag
def paginate_url(value, urlencode=None):
    """Build the pagination url."""
    get_query = f"page={value}"
    if urlencode:
        qs = urlencode.split("&")
        _filtered = filter(lambda p: p.split("=")[0] != "page", qs)
        querystring = "&".join(_filtered)
        get_query = f"{get_query}&{querystring}"
    return get_query
