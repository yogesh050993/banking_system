from django.urls import path

from customer import views

app_name = 'customer'

urlpatterns = [
    path('trx_page/', views.CustomerTransaction.as_view(), name='trx_page'),
    path('check_bal/', views.CheckBalance.as_view(), name='check_bal'),
]