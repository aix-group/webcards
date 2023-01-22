from django.urls import path

from . import views

app_name = 'mc_and_datasheet'

urlpatterns = [
    path('', views.home , name='home'), # this is home page when you dont put any path
    path('<int:id>/', views.section, name='section'),
    path('create/',views.create , name='create'),
    
]