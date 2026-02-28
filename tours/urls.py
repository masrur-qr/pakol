from tours import views
from django.contrib import admin
from django.urls import path
from django.conf.urls import url, include
from tours.views import * #ToursView, OfferedToursView
from django.views.generic.base import TemplateView

app_name = 'tours'

urlpatterns = [
    # path('',views.indexTours, name='indexTours'),  
    # url(r'^$', views.filter_tours, name='filter_tours'),
    url(r'^$', ToursView.as_view(), name='tours'),
    # path('destinations/', destinations, name='destinations'),
    # path('destinations/<slug:Slug>/', destinationViewer, name='destinationViewer'),

    path('<slug:Slug>/', activities, name='tourActivity'), 

    url(r'^offers/$', OfferedToursView.as_view(), name='offeredTours'),

    # url(r'^tour-(?P<id>\d+)/(?P<Slug>[-\w+]+)/$', views.details, name='details'),
    url(r'^(?P<Slug>[-\w+]+)$', views.details, name='details'),
    url(r'^filter/$', views.filter_tours), 
    # url(r'^booking-tour-(?P<id>\d+)/$', views.bookingg, name='bookingg'), 
    # url(r'^booking-tour/send-request/$', views.send_request, name='send_request'), # by clicking on button it is confirmed

    url(r'^booking/$', views.booking, name='booking'), #book using tour id
    url(r'^book-tour/$', views.bookTourByDepartureID, name='bookTourByDepartureID'), #book using departure id
    path('send-request', views.send_request, name='send_request'), # send the form to email if correct
    path('send-request/success', 
        TemplateView.as_view(template_name='tours/booking-success.html'), name='requestSuccess'),
    # url(r'^booking/success/$', TemplateView.as_view(template_name='tours/booking-success.html')),
    

]