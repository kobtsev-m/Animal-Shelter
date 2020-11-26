from django.urls import path
from gallery import views


app_name = 'gallery'
urlpatterns = [
    path('', views.PetList.as_view(), name='home'),
    path('create/', views.PetCreate.as_view(), name='pet-create'),
    path('<int:pk>/', views.PetDetail.as_view(), name='pet-detail'),
]