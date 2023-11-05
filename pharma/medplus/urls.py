# medplus/urls.py

from django.urls import path, include
from medplus import admin, views

urlpatterns = [
    path('about/', views.about, name='about'),
    path('thanks/',views.thanks,name='thanks'),
    path('', views.home, name='home'),
    path('prescription/', views.prescription, name='prescription'),
    path('checkout/', views.checkout, name='checkout'),
    path('cart/', views.view_cart, name='cart'),

    path('add-to-cart/<int:medicine_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('<slug:cat_slug>/<med_slug>/', views.med_details, name='medicine_details'),
    path('shipping/', views.shipping, name='shipping'),
    path('search/', views.search, name='search'),
    path('address/', views.address, name='address'),
    path('profile/', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('<slug:cat_slug>/', views.home, name='med_by_cat'),

]
