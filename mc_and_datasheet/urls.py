from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


from . import views

app_name = 'mc_and_datasheet'

urlpatterns = [
    path('', views.home , name='home'), # this is home page when you dont put any path
    path('<int:id>/', views.section, name='section'),
    path('create/',views.create , name='create'),
    path('<int:id>/file_list', views.file_list, name='file_list'),
    path('dt_section/<int:id>', views.datasheet_section, name='dt_section'),
    path('delete/<int:id>',views.delete , name='delete'),
    path('createoutput/<int:id>',views.createoutput , name='createoutput'),
    path('datasheet_export/<int:id>',views.datasheet_export , name='datasheet_export'),

]




if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)