from django.contrib.auth.views import LogoutView
from django.urls import path

from user_master import views

app_name = 'user_master'

urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('logout/', LogoutView.as_view(), name='logout'),
]