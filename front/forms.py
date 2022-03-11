


from ast import Mod
from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from django.forms import ModelForm
from razorpay import Payment

from front.models import Item,Order, Payments
PAYMENT_OPTION=(
    ('R','RazorPay'),
    ('P','PayPal')
)
PAYMENT_STATUS=(
    ('True','Paid'),
    ('False','Not Paid')
)

# countries_flag_url='//flags.example.com/{code}.png',
class CheckoutForm1(forms.Form):
    street_address=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'123 Main Street'}))
    appartment_address=forms.CharField(required=False,widget=forms.TextInput(attrs={'placeholder':'123 Main Street'}))
    country=CountryField( blank_label='(Select Country)').formfield(widget=CountrySelectWidget(attrs={
       ' class':"custom-select d-block w-100"
    }))
    zip=forms.CharField(max_length=10)
    same_shipping_address=forms.BooleanField(required=False,widget=forms.CheckboxInput())
    same_info=forms.BooleanField(required=False,widget=forms.CheckboxInput())
    payment_option=forms.ChoiceField(widget=forms.RadioSelect,choices=PAYMENT_OPTION)
class CheckoutForm(forms.Form):
    shipping_street_address=forms.CharField(required=False)
    shipping_appartment_address=forms.CharField(required=False)
    shipping_country=CountryField( blank_label='(Select Country)').formfield(required=False,widget=CountrySelectWidget(attrs={
       ' class':"custom-select d-block w-100 " 
    }))
    shipping_zip=forms.CharField(required=False)
    set_default_shipping=forms.BooleanField(required=False)
    same_shipping_address=forms.BooleanField(required=False,widget=forms.CheckboxInput())
    # same_info=forms.BooleanField(required=False,widget=forms.CheckboxInput())
    billing_street_address=forms.CharField(required=False)
    billing_appartment_address=forms.CharField(required=False)
    billing_country=CountryField( blank_label='(Select Country)').formfield(required=False,widget=CountrySelectWidget(attrs={
       ' class':"custom-select d-block w-100  "
    }))
    billing_zip=forms.CharField(required=False)
    set_default_billing=forms.BooleanField(required=False)
    same_billing_address=forms.BooleanField(required=False,widget=forms.CheckboxInput())
    use_default_billing=forms.BooleanField(required=False)
    use_default_shipping=forms.BooleanField(required=False)
    payment_option=forms.ChoiceField(widget=forms.RadioSelect,choices=PAYMENT_OPTION)
    
class CouponForm(forms.Form):
    code=forms.CharField(max_length=30,widget=forms.TextInput(attrs={ 
        'class':'form-control',
        'placeholder':'Promo Code',
        'aria-label':'Recipient"s username',
        'aria-describedby':"basic-addon2"
        
        }))
class RefundForm(forms.Form):
    ref_code=forms.CharField()
    message=forms.CharField(widget=forms.Textarea(attrs={
        'rows':4
    }))
    email=forms.EmailField()
# from betterforms.multiform import MultiModelForm
class AddItem(ModelForm):
   class Meta:
        model=Item
        exclude=['slug']
        widgets={
            'description':forms.Textarea(attrs={'cols':'42','rows':'5'})
        }
          
class OrderStatusUpdate(ModelForm):

    class Meta:
        model=Order
        fields = ['order_status']
    
       
class PaymentStatusUpdate(ModelForm):
   class Meta:
        model=Payments
        fields = ['paid']

#Customizing django allauth login form
'''# yourapp/forms.py

from allauth.account.forms import LoginForm

class YourLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(YourLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(attrs={'type': 'email', 'class': 'yourclass'})
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'yourclass'})

'''
from allauth.account.forms import LoginForm

class DjangoAllAuthLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(DjangoAllAuthLoginForm, self).__init__(*args, **kwargs)
        #type="email_text"=> allow to enter both and email and username
        self.fields['login'].widget = forms.TextInput(attrs={'type': 'email_text', 'class': 'form-control','placeholder':'Enter Email or Username'})
        self.fields["login"].label = "Username or Email"#changing login label to username or email in form
        self.fields['password'].widget = forms.PasswordInput(attrs={'class': 'form-control','placeholder':'Enter password'})