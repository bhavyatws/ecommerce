from django.urls import path
from .import views
from .views import HomeView,ItemDetailView, OrderSummary,CheckOutView,RequestRefundView


urlpatterns = [
    # path('', views.home,name="home"),
    path('', HomeView.as_view(),name="home"),
    path('product/<slug>/', ItemDetailView.as_view(),name="product"),
    path('order-summary', OrderSummary.as_view(),name="order-summary"),
    path('signin/', views.signin,name="login"),
    path('register/', views.signup,name="signup"),
    path('logout/', views.signout,name="logout"),
    # path('product-detail/<int:pk>/',views.product_detail,name="product_detail"),
    path('add-to-cart/<slug>/',views.add_to_cart,name="add-to-cart"),
    path('remove-from-cart/<slug>/',views.remove_from_cart,name="remove-from-cart"),
    path('remove-single-item-from-cart/<slug>/',views.remove_single_item_from_cart,name="remove-single-item-from-cart"),
    path('checkout/',CheckOutView.as_view(),name="check_out"),
    path('payment/',views.payment,name="payment"),
    path('paymenthandler/', views.paymenthandler, name='paymenthandler'),
    path('add-coupon/', views.add_coupon_code, name='add-coupon'),
    path('request-refund/', RequestRefundView.as_view(), name='request-refund'),
    path('search/', views.search, name='search'),
    path('filter-shirt/<slug:data>/',  views.filter_function, name='filter-shirt'),
    path('filter-sport/<slug:data>/',  views.filter_function, name='filter-sport'),
    path('filter-outwear/<slug:data>/',  views.filter_function, name='filter-outwear'),
    path('admin-dashboard/',  views.admin_dashboard, name='admin_dashboard'),
    path('admin-add-item/',  views.admin_add_item, name='admin-add-item'),
    path('update-order-status/<str:pk>',  views.update_order_status, name='update-order-status'),
    path('update-payment-status/<str:pk>',  views.update_payment_status, name='update-payment-status'),
    path('track-order/',  views.track_order, name='track-order'),
    
]
