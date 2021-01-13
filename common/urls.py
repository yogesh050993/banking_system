from django.urls import path

from common import views

app_name = 'common'

urlpatterns = [
    path('check_email/', views.check_email, name='check_email'),
    path('admin_home/', views.AdminHome.as_view(), name='admin_home'),
    path('download_report/', views.render_to_excel_report, name='download_report'),
]