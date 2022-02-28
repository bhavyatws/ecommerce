from django import template
from front.models import Order
register=template.Library()

@register.filter
def cart_item_count(user):
    if user.is_authenticated:
        qs=Order.objects.filter(user=user,ordered=False)
        if qs.exists():
            #q[0] means graving that query
            return qs[0].items.count()
    return 0
