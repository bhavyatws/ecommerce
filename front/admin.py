from django.contrib import admin
from . models import *
# Register your models here.
#Admin Function
def make_refund_accepted(modeladmin,request,queryset):
    return queryset.update(refund_requested=False,refund_granted=True)
make_refund_accepted.short_description='Update orders to refund granted'


class OrderAdmin(admin.ModelAdmin):
    list_display=['user','ordered','received','being_delivered','refund_requested','refund_granted']
    list_filter=['ordered','received','being_delivered','refund_requested','refund_granted']
    # list_display_links=['user','billing_address','coupon','payment']
    search_fields=['user__username','ref_code']#if user__username not then icontains error come
    actions=[make_refund_accepted]#custom admin action

class AddressAdmin(admin.ModelAdmin):
    list_display=[
        'user','street_address','appartment_address','country','zip','address_type','default'
    ]
    list_filter=['default','address_type','country']
    search_fields=['user__username','zip','street_address','country']
admin.site.register(Address,AddressAdmin)
admin.site.register((Payments,Item,OrderItem,
Coupon,Refund,Customer

))
admin.site.register(Order,OrderAdmin)#Here we customizing Order display in admin panel