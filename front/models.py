

from email.policy import default
from lib2to3.refactor import MultiprocessingUnsupported
from statistics import mode
from tabnanny import verbose
from xml.dom.pulldom import default_bufsize
from MySQLdb import Timestamp
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from django.shortcuts import reverse
from django_countries.fields import CountryField
category = (
    ("Electronics", "Electronics"),
    ("Sports", "Sports"),
    ("Cloth", "Cloth"),
   
    
)
status = (
    ("Accepted", "Accepted"),
    ("Packed", "Packed"),
    ("On the way", "On the way"),
    ("Delivered", "Delivered"),
    ("Cancel", "Cancel"),
   
    
)
# Create your models here.
class Customer(AbstractUser):#Users is customer here
    phone=models.CharField(max_length=12,default="")
    gender=models.CharField(max_length=15,default="")
    user_address=models.CharField(max_length=50,default="")
    def __str__(self):
        return self.username
# class Product(models.Model):
#     user=models.ForeignKey(Customer,on_delete=models.CASCADE)
#     # prod_id=models.IntegerField(primary_key=True,unique=True)
#     prod_name=models.CharField(max_length=50)
#     prod_desc=models.TextField(blank=True)
#     prod_price=models.IntegerField(default=0)
#     prod_img=models.ImageField(upload_to='Images')
#     category=models.CharField(max_length=100,choices=category,default="Unknown")
#     def __str__(self):
#         return self.prod_name
# class Cart(models.Model):
#     user=models.ForeignKey(Customer,on_delete=models.CASCADE)
#     prod=models.ManyToManyField(Product)
#     # cart=models.PositiveIntegerField(default=0)
#     def __str__(self):
#         return str(self.id)
# class OrderAndReturn(models.Model):
#     user=models.ForeignKey(Customer,on_delete=models.CASCADE)
#     prod=models.ManyToManyField(Product)
#     quantity=models.PositiveBigIntegerField()
#     date_orderplaced=models.DateTimeField(auto_now=True)
#     returned_product=models.CharField(max_length=150)
#     def __str__(self):
#         return self.user.first_name + ' -' + self.prod.prod_name
# class Payment(models.Model):
#     user=models.ForeignKey(Customer,on_delete=models.CASCADE)
#     order=models.ForeignKey(OrderAndReturn,on_delete=models.CASCADE)
#     prod=models.ManyToManyField(Product)
#     amount=models.PositiveIntegerField()
#     payment_date=models.DateTimeField(auto_now=True)
#     def __str__(self):
#         return self.order + self.prod.prod_name + " By " + self.user.first_name
# class Status(models.Model):
#     order=models.ManyToManyField(OrderAndReturn)
#     user=models.ForeignKey(Customer,on_delete=models.CASCADE)
#     status=models.CharField(max_length=50,choices=status,default="Pending")
#     payment_date=models.DateTimeField(default=now())
#     class Meta:
#         ordering = ['status']
#     def __str__(self):
#         return self.status 
LABEL_CHOICES=(
    ('S','secondary'),
    ('P','primary'),
    ('D','danger'),
)
CATEGORY_CHOICES=(
    ('S','Shirt'),
    ('SW','Sport Wear'),
    ('OW','Out Wear'),
)
ADDRESS_CHOICES=(
    ('B','Billing Address'),
    ('S','Shipping Address'),
   
)
class Item(models.Model):
    title=models.CharField(max_length=50)
    price=models.FloatField()
    discount_price=models.FloatField(blank=True,null=True)
    category=models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    label=models.CharField(choices=LABEL_CHOICES,max_length=1)
    slug=models.SlugField()
    description=models.TextField()
    image=models.ImageField(upload_to='Images',null=True,blank=True)
    def get_absolute_url(self):
        return reverse("product", kwargs={"slug": self.slug})
    def get_add_to_cart(self):
        return reverse("add-to-cart", kwargs={"slug": self.slug})
    def get_remove_from_cart(self):
        return reverse("remove-from-cart", kwargs={"slug": self.slug})
    def __str__(self):
        return self.title
class OrderItem(models.Model):
    user=models.ForeignKey(Customer,on_delete=models.CASCADE,null=True,blank=True)
    ordered=models.BooleanField(default=False)
    item=models.ForeignKey(Item,on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)
    def __str__(self):
        return f"{self.quantity} of {self.item.title}"
    def get_total_item_price(self):
        totalprice=self.item.price * self.quantity
        return totalprice
    def get_total_item_discount_price(self):
        totalprice=self.item.discount_price * self.quantity
        return totalprice
    def get_saved_amount(self):
        total_amount=self.get_total_item_price() - self.get_total_item_discount_price()
        return total_amount
    def get_final_price(self):
        if self.item.discount_price:
            return self.get_total_item_discount_price()
        return self.get_total_item_price
    
class Order(models.Model):
    user=models.ForeignKey(Customer,on_delete=models.CASCADE)
    ref_code=models.CharField(max_length=20,blank=True,null=True)
    items=models.ManyToManyField(OrderItem)
    start_date = models.DateTimeField(auto_now_add=True)
    ordered_date=models.DateField()
    ordered=models.BooleanField(default=False)
    billing_address=models.ForeignKey('Address',related_name='billing_address',on_delete=models.SET_NULL,blank=True,null=True)
    shipping_address=models.ForeignKey('Address',related_name='shipping_address',on_delete=models.SET_NULL,blank=True,null=True)
    payment_detail=models.ForeignKey('Payments',on_delete=models.SET_NULL,blank=True,null=True)
    coupon=models.ForeignKey('Coupon',on_delete=models.SET_NULL,blank=True,null=True)
    being_delivered=models.BooleanField(default=False)
    received=models.BooleanField(default=False)
    refund_requested=models.BooleanField(default=False)
    refund_granted=models.BooleanField(default=False)
    def __str__(self):
        return self.user.username
    def total_amount(self):
        total=0
        for order_item in self.items.all():
            total += order_item.get_final_price()
        if self.coupon:
            total-=self.coupon.amount 
        return total
  
    
class Address(models.Model):
    user=models.ForeignKey(Customer,on_delete=models.CASCADE)
    street_address=models.CharField(max_length=100)
    appartment_address=models.CharField(max_length=100)
    country=CountryField(multiple=False)
    zip=models.CharField(max_length=10)
    address_type=models.CharField(max_length=1,choices=ADDRESS_CHOICES)
    default=models.BooleanField(default=False)
    def __str__(self):
        return self.user.username
    class Meta:
        verbose_name_plural='Addresses'#Renaming Admin Panel name from Addresss to Addresses
class Payments(models.Model):
    razorpay_id=models.CharField(max_length=50)
    user=models.ForeignKey(Customer,on_delete=models.SET_NULL,null=True,blank=True)
    amount=models.FloatField()
    timestamp=models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.user.username

class Coupon(models.Model):
    code=models.CharField(max_length=15)
    amount=models.FloatField()
    def __str__(self):
        return self.code

class Refund(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE)
    reason=models.TextField()
    accepted=models.BooleanField(default=False)
    email=models.EmailField()
    def __str__(self):
        return f"{self.pk}"
