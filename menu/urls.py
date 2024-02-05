from django.urls import path
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('menu/', views.menu, name='menu'),
    path('catering/', views.catering, name='catering'),
    path('order/', views.order, name='order'),
    path('gallery/', views.gallery, name='gallery'),
    path('glendale/', views.Glendale, name='Glendale'),
    path('panoramacity/', views.Panorama_City, name='Panorama_City'),
    path('reseda/', views.Reseda, name='Reseda'),
    path('cart/', views.view_cart, name='view_cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    
    #path('create-checkout-session',views.payment_with_stripe,name='stripe_payment')
    # other URL patterns
]
