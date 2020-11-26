from django.urls import path, re_path
from main import views

app_name = 'main'
urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about/', views.About.as_view(), name='about'),
    re_path(r'^favicon\.ico$', views.Favicon.as_view())
]
