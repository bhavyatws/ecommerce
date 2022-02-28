from django.urls import path
from . import views

urlpatterns = [
    path('', views.home,name="home"),
    path('login/', views.signin,name="login"),
    path('register/', views.signup,name="signup"),
    path('logout/', views.signout,name="logout"),
]
