from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from attendance import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(template_name='attendance/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('qr-generator/', views.qr_generator_view, name='qr_generator'),
    path('attend/<uuid:token>/', views.attend_view, name='attend'),
    path('confirm/<uuid:token>/', views.confirm_view, name='confirm'),
    path('confirmed/', views.thank_you_view, name='thank_you'),
    path('dates/', views.date_list_view, name='date_list'),
    path('view-students/<uuid:external_token>/', views.student_list_view, name='student_list'),
    path('', views.home_view, name='home'),
]
