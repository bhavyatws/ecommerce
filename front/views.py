


from random import random

from django.utils import timezone
from django.http import HttpResponse
from django.shortcuts import redirect, render,get_object_or_404,redirect
from . models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.views.generic import ListView,DetailView,View
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import *
import stripe 
stripe.api_key = "sk_test_51KTl3sSJeQrNghIMiMkC9YcSyEGnDxbhOSMqguGCKmmrnLSN687jOmk4BMceacc09u4OnhMBm7toqpRDhSC6UZaX005lWtQnsN"
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest
from django.db.models import Q
from django.db.models import Sum#for aggregate function
# Create your views here.
import random
import string
import datetime
#Creating random generator string function
def create_ref_code():
    return ''.join(random.choices(string.ascii_lowercase+string.digits,k=20))#k=length
#
# def home(request):
#     shirt=Item.objects.filter(category='S')
#     sport_wear=Product.objects.filter(category='SW')
#     out_wear=Product.objects.filter(category='OW')
#     item=Item.objects.all()
#     context={'shirt':shirt,'sport_wear':sport_wear,'out_wear':out_wear,'item':item}
#     return render(request,'ecommerce/home-page.html',context)

class HomeView(LoginRequiredMixin,ListView):
    model=Item
    paginate_by=5
    template_name='ecommerce/home-page.html'

class ItemDetailView(LoginRequiredMixin,DetailView):
    model=Item
    template_name='ecommerce/product-page.html'

class OrderSummary(LoginRequiredMixin,View):
    
    def get(self,args,**kwargs):
        try:
            order=Order.objects.filter(user=self.request.user,ordered=False)
            empty=len(order)
            # order.total_amount()
            context={'orders':order,'empty':empty}
            return render(self.request,'Ecommerce/order_summary.html',context)
        except ObjectDoesNotExist:
            messages.success(self.request,"You donot have active order")
            return redirect("/")


    
    
def signin(request):
    if request.method == "POST":
        username=request.POST.get("username")
        password=request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
      
        if user is not None:
            login(request,user)
           
            return redirect('/')
            
        else:
            messages.error(request,"Username or Password cannot be blank")
        

    return render(request,'login.html')
# @login_required('login')   
def signout(request):
    logout(request)
    messages.success(request,"Successfully logout")
    return redirect('/')
    
    
def signup(request):
    if request.method == "POST":
        email=request.POST.get("email")
        fullname=request.POST.get("fullname")
        phone=request.POST.get("phone")
        gender=request.POST.get("radio")
        address=request.POST.get("address")
        password1=request.POST.get("password1")
        password2=request.POST.get("password2")
        user=Customer.objects.create_user(username=email,first_name=fullname,password=password1,phone=phone,gender=gender,address=address)
        user.save()
        return redirect('/')
    
    return render(request,'register.html')

# def product_detail(request,pk):
#     query=Product.objects.filter(id=pk)
#     if query.exists():
#         query=Product.objects.get(id=pk)
#         context={'query':query}
#         return render(request,'ecommerce/product-page.html',context)
#     else:
#         return redirect('/')
def buy_now(request):#checkout
    pass
# def add_to_cart(request,pk):
#     user=request.user
#     prod_id=request.GET.get('prod_id')
#     print(user,prod_id)
#     cart=Cart(user=user)
#     cart.save()
#     # prod=Product.objects.all()
#     # prod=prod.prod_id
#     cart.prod.add(prod_id)
#     user=request.user
#     query=Cart.objects.filter(user=user)
    
#     context={'query':query}
#     return render(request,'bootstrap_templates/cart.html',context)
# @login_required("login")
def add_to_cart(request,slug):
    item=get_object_or_404(Item,slug=slug)
    order_item,created=OrderItem.objects.get_or_create(item=item,
    user=request.user,
    ordered=False) #because it returning tuple
    order_query=Order.objects.filter(user=request.user,ordered=False)
    if order_query.exists():
        order=order_query[0]
        #checking if the order item is in Order
        if order.items.filter(item__slug=item.slug).exists():
            order_item.quantity+=1
            order_item.save()
            messages.success(request,"This item's quantity has been updated in your cart")
        else:
            order.items.add(order_item)
            messages.success(request,"This item has been added to your cart")
    else:
        ordered_date=timezone.now()
        order=Order.objects.create(user=request.user,ordered_date=ordered_date)
        order.save()
        order.items.add(order_item)
        messages.success(request,"This item has been added to your cart")
    # prod_id=request.GET.get('prod_id')
    # print(user,prod_id)
    # cart=Cart(user=user)
    # cart.save()
    # prod=Product.objects.all()
    # prod=prod.prod_id
    # cart.prod.add(prod_id)
    # user=request.user
    # query=Cart.objects.filter(user=user)
    # context={'query':query}
    # return render(request,'bootstrap_templates/cart.html',context)
    # return redirect("product",slug=slug)
    return redirect("order-summary")
@login_required(login_url="login/")
def remove_from_cart(request,slug):
    item=get_object_or_404(Item,slug=slug)
    order_query=Order.objects.filter(user=request.user,ordered=False)
    if order_query.exists():
        order=order_query[0]#=> graving that 
        #checking if the order item is in Item
        if order.items.filter(item__slug=item.slug).exists():
            order_item=OrderItem.objects.filter(item=item,user=request.user,ordered=False)[0] #because it returning tuple
            order.items.remove(order_item)
            
          
    
            messages.success(request," Item deleted from  your cart")
            # print(order_item.quantity)
            # order_item.save()
            
        else:
            # order_item=OrderItem.objects.filter(item=item,user=request.user,ordered=False)[0]
            # print(order_item)
            # print(order_item.quantity)
            # if order_item.quantity==0:
            #     order.delete()
            #     order_item.delete()
            messages.success(request,"This item doesnot exist in your cart")
            # return redirect("product",slug=slug)
            return redirect("order-summary")
    
    else:    
        messages.success(request,"You donot have active item in cart")
        # return redirect("product",slug=slug)
        return redirect("order-summary")
    # return redirect("product",slug=slug)
    return redirect("order-summary")
@login_required(login_url="login/")
def remove_single_item_from_cart(request,slug):
    item=get_object_or_404(Item,slug=slug)
    order_query=Order.objects.filter(user=request.user,ordered=False)
    if order_query.exists():
        order=order_query[0]#=> graving that 
        #checking if the order item is in Item
        if order.items.filter(item__slug=item.slug).exists():
            order_item=OrderItem.objects.filter(item=item,user=request.user,ordered=False)[0] #because it returning tuple
            if order_item.quantity>1:
                order_item.quantity-=1
                order_item.save()
            else:
                order.items.remove(order_item)
                order.delete()
                order_item.delete()
          
    
            messages.success(request," This item's quantity has been removed your cart")
            # print(order_item.quantity)
            # order_item.save()
            
        else:
           
           
                
            messages.success(request,"This item doesnot exist in your cart")
            return redirect("order-summary")
    
    else:    
        messages.success(request,"You donot have active item in cart")
        return redirect("order-summary")
    return redirect("order-summary")

def show_cart(request):
    pass

def is_valid_form(values):#values is list here
    valid=True
    for field in values:
        if field=='':#checking if empty string
            valid=False
    return valid

class CheckOutView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        try:
            form=CheckoutForm()
            coupon=CouponForm()
            orders=Order.objects.filter(user=self.request.user,ordered=False)
            context={'form':form,'orders':orders,'coupon':coupon}
            shipping_address_qs=Address.objects.filter(
                user=self.request.user,
                address_type='S',
                default=True
            )
            if shipping_address_qs.exists():
                context.update({'default_shipping_address':shipping_address_qs[0]})
            billing_address_qs=Address.objects.filter(
                user=self.request.user,
                address_type='B',
                default=True
            )
            if billing_address_qs.exists():
                context.update({'default_shipping_address':billing_address_qs[0]})
            return render(self.request,'Ecommerce/checkout-page.html',context)

        except ObjectDoesNotExist:
            messages.info(self.request,"You donot have active order")
            return redirect("checkout")
    def post(self,*args,**kwargs):
        form=CheckoutForm(self.request.POST or None)
        order=Order.objects.get(user=self.request.user,ordered=False)
        try:
            if form.is_valid():
                use_default_shipping=self.request.POST.get('use_default_shipping')
                if use_default_shipping:
                    print("using default shipping")
                    address_qs=Address.objects.filter(
                        user=self.request.user,
                        address_type='S',
                        default=True
                        )
                    if address_qs.exists():
                        shipping_address=address_qs[0]
                        order.shipping_address=shipping_address
                        order.save()
                    else:
                        messages.info(self.request,"No default shipping address availabel")
                        return redirect("check_out")
                else:
                    print("User is entering new shipping address")

                        
                    shipping_address1=self.request.POST.get('shipping_address1')
                    print(shipping_address1)
                    shipping_address2=self.request.POST.get('shipping_address2')
                    print(shipping_address2)
                    shipping_country=form.cleaned_data.get('shipping_country')
                    shipping_zip=self.request.POST.get('shipping_zip')
                    if is_valid_form([shipping_address1,shipping_address2,shipping_country,shipping_zip]):
                        shipping_address=Address(
                        user=self.request.user,
                        street_address=shipping_address1,
                        appartment_address=shipping_address2,
                        country=shipping_country,
                        zip= shipping_zip,
                        address_type='S'
                        )
                        
                        shipping_address.save()
                        order.shipping_address=shipping_address
                        order.save()
                        set_default_shipping=self.request.POST.get("set_default_shipping")
                        if set_default_shipping:
                            shipping_address.default=True
                            shipping_address.save()
                    else: 
                        messages.info(self.request,'Please fill required fields of form')
                
                    use_default_billing=self.request.POST.get('use_default_billing')
                    same_billing_address=self.request.POST.get('same_billing_address')
                    if same_billing_address:
                        billing_address=shipping_address
                        billing_address.pk=None
                        billing_address.save()
                        billing_address.address_type='B'
                        billing_address.save()
                        order.billing_address=billing_address
                        order.save()
                        
                    elif use_default_billing:
                        print("using default billing")
                        address_qs=Address.objects.filter(
                            user=self.request.user,
                            address_type='B',
                            default=True
                        )
                        if address_qs.exists():
                            billing_address=address_qs[0]
                            order.billing_address=billing_address
                            order.save()
                        else:
                            messages.info(self.request,"No default billing address availabel")
                            return redirect("check_out")
                    else:
                        print("User is entering new billing address")

                        
                        billing_address1=self.request.POST.get('billing_address1')
                        billing_address2=self.request.POST.get('billing_address2')
                        billing_country=self.request.POST.get('billing_country')
                        billing_zip=self.request.POST.get('billing_zip')
                        if is_valid_form([billing_address1,billing_address2,billing_country,billing_zip]):
                            billing_address=Address(
                            user=self.request.user,
                            street_address=billing_address1,
                            appartment_address=billing_address2,
                            country=billing_country,
                            zip= billing_zip,
                            address_type='B'
                            )
                            billing_address.save()
                            order.address=billing_address
                            order.save()
                            set_default_shipping=self.request.POST.get("set_default_shipping")
                            if set_default_shipping:
                                billing_address.default=True
                                billing_address.save()
                        else: 
                            messages.info(self.request,'Please fill required fields of form')
                    
                    payment_option=self.request.POST.get('payment_option')
            
                    #TODO:Add Function Functionality
                    # saving_info=form.cleaned_data.get('saving_info')
                    # same_shipping_address=form.cleaned_data.get('saving_shipping_address')
                    payment_info=self.request.POST.get('payment_info')
                #     print(street_address,appartment_address,country,zip,payment_option)
                #     billing_address=Address(
                #     user=self.request.user,
                #     street_address=street_address,
                #     appartment_address=appartment_address,
                #     country=country,
                #     zip= zip,
                #     address_type='B'
                #     )
                # billing_address.save()
                # order.address=billing_address
                # order.save()
                
                # Checking which payment method has been used and redirecting to that page
                if payment_option=="R":
                    return redirect("payment")
                elif payment_option=="P":
                    return redirect("check_out")
                else:
                    return redirect("order-summary")
                # #TODO Redirecting to selected Payment
                # return redirect("payment")
            messages.warning(self.request,"Failed Checkout")
            return redirect("check_out")
        except ObjectDoesNotExist:
            messages.success(self.request,"You donot have active order")
            return redirect("order-summary")
        
       




# authorize razorpay client with API Keys.
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

@login_required(login_url="login/")
def payment(request):
    # print("User:",request.user)
    order=Order.objects.get(user=request.user,ordered=False)
   
    print(order.id)
    currency ='INR'
    amount = order.total_amount() * 100# 1Rs=100Paisa
# Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                    currency=currency,
                                                    payment_capture='1'))
                                                    #payment_capture must true i.e 1
    
    
    # order id of newly created order.
    razorpay_order_id = razorpay_order['id']
    from django.contrib.sites.shortcuts import get_current_site
    callback_url ='http://'+ str(get_current_site(request))+"/paymenthandler/"
    print(callback_url)
    # callback_url='paymenthandler/'
    # we need to pass these details to frontend.
    context = {}
    context['razorpay_order_id'] = razorpay_order_id
    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
    context['razorpay_amount'] = amount
    context['currency'] = currency
    context['callback_url'] = callback_url
    context['email']=order.user.username
    context['name']=order.user.first_name
    context['phone']=order.user.phone
    

    payment=Payments(
        razorpay_id=razorpay_order['id'],
        user=request.user,
        amount=order.total_amount(),
    )
    payment.save()
    #Working on Order
    order_items=order.items.all()
    order_items.update(ordered=True)
    for item in order_items:
        item.save()
    order.ordered=True
    order.ref_code=create_ref_code()
    order.payment_detail=payment
    order.save()

    messages.success(request,"Your order was successful")
    return render(request, 'Ecommerce/payment.html', context=context)


# we need to csrf_exempt this url as
# POST request will be made by Razorpay
# and it won't have the csrf token.
@csrf_exempt
@login_required(login_url="login/")
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

        

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)

            if result :
                # print(result)
                # amount = 2000

                # order.total_amount() * 100 #

                # capture the payemt
                # razorpay_client.payment.capture(payment_id, amount)

                # render success page on successful caputre of payment
                return render(request, 'Ecommerce/payment_success.html')
            else:

                # if signature verification fails.
                return render(request, 'Ecommerce/payment_fail.html')
    else:
    # if other than POST request is made.
        return HttpResponseBadRequest()

def get_coupon(request,code):
    try:
        coupon=Coupon.objects.get(code=code)
        return coupon
    except ObjectDoesNotExist:
        messages.info(request,"This coupon doesnot exist")
        return redirect("check_out")
@login_required(login_url="login/")
def add_coupon_code(request):
    if request.method=="POST":
        form=CouponForm(request.POST or None)
        if form.is_valid():
            try:
                code=form.cleaned_data.get('code')
                order=Order.objects.get(user=request.user,ordered=False)
                coupon=get_coupon(request,code)
                order.coupon=coupon
                order.save()
                messages.success(request,"Coupon Successfully Applied")
                return redirect("check_out")
            except ObjectDoesNotExist:
                messages.info(request,"You donot have active item in your cart")
                return redirect("check_out")
    else:
        return render(request,'Ecommerce/order_snippet.html',{'form':CouponForm()})
class RequestRefundView(LoginRequiredMixin,View):
    def get(self,*args,**kwargs):
        form=RefundForm()
        context={'form':form}
        return render(self.request,'Ecommerce/request_refund.html',context=context)
    def post(self,*args,**kwargs):
        form=RefundForm(self.request.POST)
        if form.is_valid():
            ref_code=form.cleaned_data.get('ref_code')
            message=form.cleaned_data.get('message')
            email=form.cleaned_data.get('email')
            try:
                order=Order.objects.get(ref_code=ref_code)
                order.refund_requested=True
                order.save()
                #store the refund 
                refund=Refund()
                refund.order=order
                refund.reason=message
                refund.email=email
                refund.save()
                messages.info(self.request,"Your refund request received")
                return redirect("request-refund")
            except ObjectDoesNotExist:
                messages.info(self.request,"This order does not exist")
                return redirect("request-refund")
@login_required(login_url="login/")
def filter_function(request,data=None):
   
   
    if data=="shirt":
        obj=Item.objects.filter(category="S")
        
    elif data=="sport-wear":
        obj=Item.objects.filter(category="SW")
    elif data=="out-wear":
        obj=Item.objects.filter(category="OW")
   
    return render(request,'Ecommerce/home-page.html',{'object_list':obj})

def search(request):
    if request.method=="GET":
        data=request.GET.get('data')
        obj=Item.objects.filter(Q(title__icontains=data)|Q(description__icontains=data))
        return render(request,'Ecommerce/home-page.html',{'object_list':obj})
    return HttpResponse("Not Found")

@login_required(login_url="login/")
def admin_dashboard(request):
    users=Customer.objects.all().count()
    total_ordered=Order.objects.filter(ordered=True).count()
    total_earning=Payments.objects.all().aggregate(Sum('amount'))
    order_pending=Order.objects.filter(order_status="Pe").count()
    orders=Order.objects.all()
    total_items=Item.objects.all().count()
    #Custom logic for fetching first_week graph total order summary
    today=datetime.datetime.now()
    last_week=today-datetime.timedelta(days=7)
    seven_days_count=[]
    seven_days_date=[]
    n=0
    while(n<7):
        last_week=last_week+datetime.timedelta(days=1)
        seven_days_date.append(last_week)
        last_seven_days_orders=Order.objects.filter(ordered_date=last_week).count()
        seven_days_count.append(last_seven_days_orders)
        n+=1
    context={'orders':orders,'users':users,'total_ordered':total_ordered,'total_earning':total_earning['amount__sum']
    ,'order_pending':order_pending,'total_items':total_items,'seven_days_count':seven_days_count,'seven_days_date':seven_days_date}
    return render(request,'Ecommerce/admin_dashboard.html',context=context)
@login_required(login_url="login/")
def admin_add_item(request):
    form=AddItem()
    form=AddItem(request.POST or None,request.FILES)
    if form.is_valid():
        form.save()
        return redirect('admin_dashboard')
    context={'form':form}
    return render(request,'Ecommerce/add_admin_item.html',context=context)
@login_required(login_url="login/")
def update_order_status(request,pk):
    type(pk)
    instance = Order.objects.get(id=pk)
    form=OrderStatusUpdate(request.POST or None,instance=instance)
    # if request.method=="POST":
    if form.is_valid():
        form.save()
        return redirect('admin_dashboard')
    context={'form':form,'pk':pk}
    return render(request,'Ecommerce/update_order_status.html',context=context)

    