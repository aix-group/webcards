from django.urls import path
from django.conf.urls.static import static
from django.conf import settings


from . import views

app_name = 'mc_and_datasheet'

urlpatterns = [
    path('', views.home , name='home'), # this is home page when you dont put any path
    path('<int:id>/', views.section, name='section'),
    #path('index/',views.index , name='index'),
    path('about/',views.about , name='about'),
    path('impressum/',views.impressum , name='impressum'),
    path('legal/',views.legal , name='legal'),
    path('contact/',views.contact , name='contact'),
    path('upload_file/<int:id>/',views.upload_file , name='upload_file'),
    path('datacard_section/<int:id>', views.datacard_section, name='datacard_section'),
    #path('blog-home/',views.blog_home , name='blog-home'),
    #path('blog-post/',views.blog_post , name='blog-post'),
    #path('portfolio-overview/',views.portfolio_overview , name='portfolio-overview'),
    #path('portfolio-item/',views.portfolio_item , name='portfolio-item'),
    path('dt_section/<int:id>', views.datasheet_section, name='dt_section'),
    path('delete/<int:id>',views.delete , name='delete'),
    path('upload_json/<int:id>',views.upload_json , name='upload_json'),
    path('createoutput/<int:id>',views.createoutput , name='createoutput'),
    path('datasheet_export/<int:id>',views.datasheet_export , name='datasheet_export'),
    #path('my-page/', views.my_view, name='my-page'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)




if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)