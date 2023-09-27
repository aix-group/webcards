from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


from . import views

app_name = 'mc_and_datasheet'

urlpatterns = [
    path('', views.home , name='home'), # this is home page when you dont put any path
    path('<int:id>/', views.section, name='section'),
    path('about/',views.about , name='about'),
    path('impressum/',views.impressum , name='impressum'),
    path('legal/',views.legal , name='legal'),
    path('contact/',views.contact , name='contact'),
    path('upload_file/<int:id>/',views.upload_file , name='upload_file'),
    path('datacard_section/<int:id>', views.datacard_section, name='datacard_section'),
    path('dt_section/<int:id>', views.datasheet_section, name='dt_section'),
    path('delete/<int:id>',views.delete , name='delete'),
    path('upload_json/<int:id>',views.upload_json , name='upload_json'),
    path('createoutput/<int:id>',views.createoutput , name='createoutput'),
    path('datasheet_export/<int:id>',views.datasheet_export , name='datasheet_export'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)