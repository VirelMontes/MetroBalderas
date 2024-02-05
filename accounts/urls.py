from django.urls import path
from . import views
from accounts.views import *

urlpatterns = [
    path('signup/', views.sign_up, name='signup'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    # path('logout/', views.logout, name='logout'),
    path('login/', views.sign_in, name='login'),
    path('logout/', views.sign_out, name='logout'),
]