from django.contrib import admin
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from tours import  views as toursViews # destinations, destinationViewer
from django.views.generic import TemplateView

app_name = 'home'
admin.site.site_header = "Pakol Travel" 

urlpatterns = [ 
    path('', views.homePage, name='homePage'), 
    path('about-us', views.aboutUs, name="aboutUs"),
    path('rentals-and-services/', views.ourServices, name="ourServices"),
    path('rentals-and-services/<slug:Slug>/', views.serviceRentalDetails, name='serviceRentalDetails'),
    path('contacts', views.contacts, name="contacts"),

    path('destinations/', toursViews.destinations, name='destinations'),
    path('send-request/', views.requestPage, name='requestPage'),
    path('send-request/success', 
        TemplateView.as_view(template_name='home/request-success.html'), name='requestSuccess'),

    path('destinations/<slug:Slug>/', toursViews.destinationViewer, name='destinationViewer'),

    path('faq', views.FAQs, name="faq"), 


] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
