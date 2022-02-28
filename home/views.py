from django.http import HttpResponse
from django.shortcuts import redirect, render
from . models import *

# Create your views here.
def home(request):
    context={}
    return render(request,'bootstrap_templates/index.html',context)
def signin(request):
    context={}
    return render(request,'login.html',context)
    
def signout(request):
    return HttpResponse("Successfully Logout")
    
def signup(request):
    if request.method == "POST":
        username=request.POST.get("username")
        fullname=request.POST.get("fullname")
        email=request.POST.get("email")
        phone=request.POST.get("phone")
        gender=request.POST.get("gender")
        address=request.POST.get("address")
        password1=request.POST.get("password1")
        password2=request.POST.get("password2")
        user=Customers.objects.create_user(username=username,first_name=fullname,email=email,password=password1,phone=phone,gender=gender,address=address)
        user.save()
        return redirect('/')
    
    return render(request,'register.html')