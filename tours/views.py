from django.shortcuts import render

from django.views.generic.base import TemplateView
from django.views.generic import TemplateView
from django.shortcuts import render, redirect,  get_object_or_404 # get_list_or_404,
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from tours.forms import CreateTourForm, SearchTourForm
from tours.models import Tour, Destination, Itinerary, Departures, PlaceAvailability
from tours.models import  BookTourForm, BookTourByDepartureIDForm
from django.contrib.auth.models import User
from django.db.models import Q
from django.conf import settings
from django.core.mail import send_mail
from django.core import mail
connection = mail.get_connection()

from django.views.generic.base import TemplateView
from django.http import HttpResponseRedirect
from django.core.mail import send_mail, BadHeaderError
from tours.models import (SearchForm, 
                        Photo, 
                        # ACTIVITIES, TOUR_TYPES,
                        TourActivities, TourTypes
                        )
# from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from home.models import SEO_Optimiser, Page
from django.urls import reverse
import datetime
# Create your views here.

# def indexTours(request):
#     return render(request, 'tours/tours-list.html') 




# Views the list of the tour 
class ToursView(TemplateView): 
    template_name = 'tours/tours-list.html'
    def get(self, request):
        # form = CreateTourForm()
        tours = Tour.objects.filter(Available=True) 

        if request.GET.get("Activity") != None:
            activity = request.GET.get('Activity')
            tours = tours.filter(TourType=activity)
        else:
            activity = False
        
        if request.GET.get("destination") != None:
            destination = request.GET.get('destination')
            tours = tours.filter(Destination__Slug=destination)
        else:
            activity = False

        myfilter = Q()
        # if request.GET.get("Activity") != None:
        #     TourType = request.GET.getlist('TourType')
        #     if TourType:
        #         ttFilter = Q()
        #     for tt in TourType:
        #         # if tt is not None:
        #         ttFilter |=  Q(tourTypes__Title__contains=tt) 
        #     myfilter &= ttFilter

        # getActivities = []
        # if request.GET.get("Activities") != None:
        #     Activities = request.GET.getlist('Activities')
        #     if Activities: #is not None: 
        #         actFilter = Q() 
        #     for activity in Activities:
        #         actFilter |=  Q(tourActivities__Slug__icontains=activity) 
        #         getActivities.append(TourActivities.objects.get(Slug__icontains=activity))
        #     myfilter &= actFilter
            

        # if request.GET.get("Title") != None:
        #     Title = request.GET.get('Title', None)
        #     if Title is not '':
        #         titleFilter = Q() 
        #         titleFilter |=  (
        #             Q (Title__contains=Title) 
        #             | Q(Destination__Area__contains=Title)
        #             | Q(Destination__Valley__contains=Title)
        #             | Q(Destination__City__contains=Title)
        #             | Q(tourTypes__Title__contains=Title)
        #             | Q(tourActivities__Title__contains=Title)
        #             # | Q(Description__contains=Title)
        #             # | Q(ShortDesc__contains=Title)
        #         )
        #         myfilter &= titleFilter

        if request.GET.get("DepartingDate") != None and request.GET.get("DepartingDate") != None:
            DepartingDate = request.GET.get('DepartingDate')
            FinishingDate = request.GET.get('FinishingDate')
            if DepartingDate != '' and FinishingDate != '':
                DepartingDate=datetime.datetime.strptime(DepartingDate, '%m/%d/%Y').strftime('%Y-%m-%d')
                FinishingDate=datetime.datetime.strptime(FinishingDate, '%m/%d/%Y').strftime('%Y-%m-%d')

                myfilter &= (Q(tour_departures__DepartingDate__gt=DepartingDate) and Q(tour_departures__FinishingDate__lt=FinishingDate))
        elif request.GET.get("DepartingDate") != None:
            DepartingDate = request.GET.get('DepartingDate')
            if DepartingDate is not '':
                myfilter &= Q(tour_departures__DepartingDate__gt=DepartingDate)
        elif request.GET.get("FinishingDate") != None:
            FinishingDate = request.GET.get('FinishingDate')
            if FinishingDate is not '':
                myfilter &= Q(tour_departures__FinishingDate__lt=FinishingDate)

        
        # if (request.GET.get("MinPrice") != None 
        #     and request.GET.get("MinPrice") != ''
        #     and request.GET.get("MaxPrice") != None
        #     and request.GET.get("MaxPrice") != ''):
        #     MinPrice = request.GET.get('MinPrice')
        #     MaxPrice = request.GET.get('MaxPrice')
        #     myfilter &= (Q(Price__gt=MinPrice) & Q(Price__lte=MaxPrice))
        
        # elif request.GET.get("MaxPrice") != None and request.GET.get("MaxPrice") != '':
        #     MaxPrice = request.GET.get('MaxPrice')
        #     myfilter &= Q(Price__lte=MaxPrice)

        # elif request.GET.get("MinPrice") != None and request.GET.get("MinPrice") != '':
        #     MinPrice = request.GET.get('MinPrice')
        #     myfilter &= Q(Price__gt=MinPrice)
        

        # tours = Tour.objects.filter(myfilter).distinct().filter(Available=True)
        # tours = Tour.objects.filter(Available=True)
        tours = tours.filter(myfilter).distinct().filter(Available=True)

        filteredToursCounter = tours.count()
        SEO = SEO_Optimiser.objects.get(seoid=1)

        # tour_types = TourTypes.objects.all()
        # tour_activities = TourActivities.objects.all()
        
        paginator = Paginator(tours, 6) # Show x tours per page
        page = request.GET.get('page')
        tours = paginator.get_page(page)
        
        # if activity not False:
        #     pass


        args = {
                'tours':tours, 
                'activity': activity,
                # 'getActivities':getActivities,
                # 'tour_types': tour_types,
                # 'tour_activities': tour_activities,
                'SEO': SEO,
                # 'ACTIVITIES': ACTIVITIES, 
                # 'TOUR_TYPES': TOUR_TYPES,
                'filteredToursCounter': filteredToursCounter, 
            }  
        return render(request, self.template_name, args )
    def post(self, request):
        TourDeparture = request.POST.get('TourDeparture','')
        tourid = int(request.POST.get('tourid'))
        tour = Tour.objects.get(id=tourid)
        name = request.POST.get('name','')
        email = request.POST.get('email','')
        tourists = request.POST.get('tourists',1)
        message = request.POST.get('message','')

        TourCode = tour.TourCode #request.POST.get('TourCode','')
        Title = tour.Title #request.POST.get('Title','')
        TourURL = tour.get_absolute_url #request.POST.get('TourURL')
        

        # if result['success']:
        fromDTP = 'info@pakoltravel.com' #'sales@pakoltravel.com'
        reciever_list= ('info@pakoltravel.com',) #info@pakoltravel.com
        # toDTP = 'info@pakoltravel.com'
        
        # Send a notofocation to client also

        
        message = "Your tour - "+ str(TourCode)+ \
        " ("+str(Title) + ") has a new request from "+str(name)+". \n\n" \
        "TOUR INFORMATION:\n" \
        "\nTour Code: "+ str(TourCode) \
        +"\nURL: https://pakoltravel.com"+str(TourURL) \
        +"\nDeparting Date: "+str(TourDeparture) \
        + "\n\nCUSTOMER DETAILS and INFORMATION:\n" \
        +"\nName: "+str(name)  \
        + "\nEmail: " + str(email)  \
        + "\nNumber of tourists: "+str(tourists) \
        + "\nMessage: "+str(message) \
        + " \n\nPlease reply to this message  during 24 hours. \n\n" \
        + "Best regards,\n\n Pakol Travel team"
        
        subject = 'Your tour - '+ str(TourCode) + ' - '+str(Title)+ ' has a new request from '+str(firstname) 

        send_mail(subject, message, fromDTP, reciever_list, fail_silently=False, )
        return HttpResponseRedirect('/tours/booking-success')
    # else:
    #     return HttpResponseRedirect('/error/')        
    #     else:
    #         return HttpResponseRedirect('/tours/invalid-booking-form/')
    # else:
    #     return HttpResponseRedirect('/tours/unknown-request-method/')

def details(request, Slug):
    if request.method == 'GET':
            
        tour=Tour.objects.get(Slug=Slug)
        obj = tour

        tour.Highlights = tour.Highlights.split(';')
        tour.Inclusions = tour.Inclusions.split(';')
        tour.Exclusions = tour.Exclusions.split(';')
        tour.ImportantNotes = tour.ImportantNotes.split(';')

        # tour.Route = tour.Route.split('-')
        # tour.PriceList = tour.PriceList.split(',')
        # tourImportantNotes = tour.ImportantNotes.split(';')
        tour.Route = tour.Route.split('-')

        # intype = tour.ImportantNotes
        #Unset the variables if they are empty
        # if tour.ImportantNotes == "":#tour.ImportantNotes[0] == "": #len(tour.ImportantNotes) == 0 or
        #     tourImportantNotes = None
        # else:
        #     tourImportantNotes = tour.ImportantNotes.split(';')

        # if not tour.ImportantNotes:
        # if tour.PriceList[0] == "":
        #     del tour.PriceList

        # trip_related = tour.tags.similar_objects()[:3]
        
        # trip = get_object_or_404(Tour, slug=Slug)
        # trip_related = trip.tags.similar_objects()
        # return render(request, 'app_trip/trip_single.html', {'trip': trip, 'trip_related': trip_related})


        photos = Photo.objects.filter(gallery=tour.Gallery)
        itineraries = Itinerary.objects.filter(tour=tour.id)

        # tid = int(id)   
        departures = Departures.objects.filter(tour=tour.id) # was ->  tour=tour.id

        # placesAvailability = PlaceAvailability.objects.all()
        placesAvailability = Departures.objects.select_related().all()#related_departure

        tourtypes = tour.TourType
        # trip_related = []
        trip_related = []  #Tour.objects.filter(TourType__in=tourtypes)#.distinct() 
        # Tour.objects.all()[:3]

        # for tr in Tour.objects.all():
        #     if tr.TourType in tourtypes:
        #         trip_related.append(tr) 

        # trip_related = trip_related[:4]

        context = {
            'tour' : tour,
            'tourtypes': tourtypes,
            # 'tourImportantNotes': tourImportantNotes,
            'photos': photos,
            'itineraries': itineraries,
            'departures': departures,
            'placesAvailability': placesAvailability,
            # 'trip': trip, 
              'trip_related': trip_related,
              'obj': obj,
        }
        return render(request, 'tours/tour-detail.html',context)
    elif request.method == 'POST':
        firstname = request.POST.get("firstname", "")
        lastname = request.POST.get("lastname", "")
        email = request.POST.get("email", "")
        message = request.POST.get("message", "")
        tour_id = request.POST.get("tourid")
        depid = request.POST.get("departure_id", "")

        tour_id = int(tour_id) 

        tourObj = Tour.objects.get(id=tour_id)
        if depid != '':
            depid = int(depid)
            try:
                departureObj = Departures.objects.get(id=depid)
                departure = str(departureObj.DepartingDate) + ' - ' + str(departureObj.FinishingDate) 
            except:
                departure = 'NA'
        else:
            departure = 'NA'

        trip_related = Tour.objects.order_by('Created')[:3]

        fromDTP = 'info@pakoltravel.com' 
        reciever_list= ('info@pakoltravel.com',) 
        subject = 'New request for the tour  - '+ str(tourObj.Title) + ' from '+ firstname 
        message = "Your tour - "+ str(tourObj.Title)+ \
            "(https://pakoltravel.com"+str(request.path) + ") has a new request. \n\n" \
            "TOUR INFORMATION:\n" \
            "\nTour Title: "+ str(tourObj.Title) \
            +"\nURL: https://pakoltravel.com"+str(request.path) \
            +"\nDeparting Date: "+str(departure) \
            + "\n\nCUSTOMER CONTACTS and MESSAGE:\n" \
            +"\nName: "+str(firstname)  \
            + "\nLast name: "+ str(lastname) \
            + "\nEmail: " + str(email)  \
            + "\nMessage: "+str(message) \
            + " \n\nPlease reply to this message  during 24 hours. \n\n" \
            + "Best regards,\n\nPakol Travel"
        # try:
        send_mail(subject, message, fromDTP, reciever_list, fail_silently=False, )
        return redirect(reverse('tours:requestSuccess'), kwargs={'trip_related': trip_related} )
        
        # return reverse('tours:requestSuccess')
        # except:
        #     return HttpResponseRedirect('/tours/booking/error/')


def activities(request, Slug):
    if request.method == 'GET':
            
        tours=Tour.objects.filter(TourType=Slug)

        paginator = Paginator(tours, 6) # Show x tours per page
        page = request.GET.get('page')
        tours = paginator.get_page(page)

        title = ' '.join(Slug.split('-')).capitalize() 

        context = {
            'tours' : tours,
            'title': title,
        }
        return render(request, 'tours/tours-list-activities.html',context)

def destinations(request):
    destinations  = Destination.objects.all()
    page =  Page.objects.get(id=8)
    SEO = page.SEO 
    context = {
        'destinations': destinations,
        'obj': page,
        'SEO': SEO,
    }
    return render(request, 'tours/destinations-list.html',context)

def destinationViewer(request, Slug):
    # if request.method == 'GET':
            
    # tours=Tour.objects.filter(Q(Destination__icontains = Slug))

    destination =  Destination.objects.get(Slug=Slug)
    destinations =  Destination.objects.filter()

    tours=Tour.objects.filter(Destination = destination.id)

    # title = ' '.join(Slug.split('-')).capitalize() 

    context = {
        'tours' : tours,
        # 'title': title,
        'obj': destination,
        'objs': destinations,
    }
    return render(request, 'tours/destination-details.html',context)



class OfferedToursView(TemplateView):
    template_name = 'tours/tours-list.html'

    def get(self, request):
        # form = CreateTourForm()
        tours = Tour.objects.filter(Available=True).filter(Offer=True)
        # destination = Destination.objects.all()

        # dest = Tour.objects.filter(id = Destination_id)
        # destination2 = Destination.objects.filter(dest = Destination_id)
        paginator = Paginator(tours, 6) # Show 9 tours per page
        page = request.GET.get('page')
        tours = paginator.get_page(page)

        filteredToursCounter = Tour.objects.all().count()
        tour_types = TourTypes.objects.all()
        tour_activities = TourActivities.objects.all()
        #users = User.objects.exclude(id=request.user.id) #v52     53 .all()
        offeredTitle = ("Offered Tours")  
        args = {
                'tours':tours, 
                'tour_types': tour_types,
                'tour_activities': tour_activities,
                # 'ACTIVITIES': ACTIVITIES, 
                # 'TOUR_TYPES': TOUR_TYPES,
                'filteredToursCounter': filteredToursCounter, 
                'offeredTitle': offeredTitle,
            } # 'destination':destination, 'form': form,
        return render(request, self.template_name, args )

# def details(request, Slug):
#     tour=Tour.objects.get(Slug=Slug)
#     tour.Highlights = tour.Highlights.split(';')
#     tour.Inclusions = tour.Inclusions.split(';')
#     tour.Exclusions = tour.Exclusions.split(';')
#     # tour.Route = tour.Route.split('-')
#     # tour.PriceList = tour.PriceList.split(',')
#     # tourImportantNotes = tour.ImportantNotes.split(';')
#     tour.Route = tour.Route.split('-')

#     # intype = tour.ImportantNotes
#     #Unset the variables if they are empty
#     if tour.ImportantNotes == "":#tour.ImportantNotes[0] == "": #len(tour.ImportantNotes) == 0 or
#         tourImportantNotes = None
#     else:
#         tourImportantNotes = tour.ImportantNotes.split(';')

#     # if not tour.ImportantNotes:
#     # if tour.PriceList[0] == "":
#     #     del tour.PriceList

#     trip_related = tour.tags.similar_objects()[:3]
#     trip_related = Tour.objects.exclude(id=tour.id).order_by('Created')[:3]

#     # trip = get_object_or_404(Tour, slug=Slug)
#     # trip_related = trip.tags.similar_objects()
#     # return render(request, 'app_trip/trip_single.html', {'trip': trip, 'trip_related': trip_related})


#     photos = Photo.objects.filter(gallery=tour.Gallery)
#     slider_photos = photos[:3]

#     itineraries = Itinerary.objects.filter(tour=tour.id)

#     # tid = int(id)   
#     departures = Departures.objects.filter(tour=tour.id) # was ->  tour=tour.id

#     # placesAvailability = PlaceAvailability.objects.all()
#     placesAvailability = Departures.objects.select_related().all()#related_departure


#     context = {
#         'tour' : tour,
#         'tourImportantNotes': tourImportantNotes,
#         'photos': photos,
#         'slider_photos':slider_photos,
#         'itineraries': itineraries,
#         'departures': departures,
#         'placesAvailability': placesAvailability,
#         # 'trip': trip, 
#         'trip_related': trip_related,

#     }
#     return render(request, 'tours/tour-detail.html',context)


def filter_tours(request, *args, **kwargs):
    # reverse('tours:tours')
    return HttpResponseRedirect(reverse('tours:tours', *args, **kwargs))

# def filter_tours(request,  *args, params=None, **kwargs):
#     query_params = ""
#     if params:
#         query_params += '?' + urlencode(params)
#     return redirect(query_params, *args, **kwargs)

# @login_required
# def booking(request, id):
#     if request.method == 'GET':
#         tour = Tour.objects.get(id=id)
#         tour.Route = tour.Route.split('-')
#         thisTourDepartures = Departures.objects.filter(tour_id = id)
#         args = { 
#             # 'tid':id,
#             'tour':tour,
#             'thisTourDepartures':thisTourDepartures
#             }
#         return render(request, 'tours/booking-form.html',  args)
#     return HttpResponseRedirect('/tours/booking-error/')

@login_required
def booking(request):
    if request.method == 'GET':
        form = BookThisForm(request.GET)
        if form.is_valid():
            tid = form.cleaned_data['tid']
            thisTourDepartures = Departures.objects.filter(tour_id = tid)
            tour = Tour.objects.get(id=tid)
            tour.Route = tour.Route.split('-')
            args = { 
                'tid':tid,
                'thisTourDepartures': thisTourDepartures,
                'tour':tour,
                }
            return render(request, 'tours/booking-form.html',  args)
    return HttpResponseRedirect('/tours/booking-error/')



# @login_required
def send_request(request):
    if request.method == 'POST':
        TourDeparture = request.POST.get('TourDeparture','')
        tourid = int(request.POST.get('tourid'))
        tour = Tour.objects.get(id=tourid)
        firstname = request.POST.get('firstname','')
        lastname = request.POST.get('lastname','')
        email = request.POST.get('email','')
        phone = request.POST.get('phone','')
        country = request.POST.get('country','')
        adults = request.POST.get('adults','')
        children = request.POST.get('children','')
        message = request.POST.get('message','')

        TourCode = tour.TourCode #request.POST.get('TourCode','')
        Title = tour.Title #request.POST.get('Title','')
        TourURL = tour.get_absolute_url #request.POST.get('TourURL')
        

        # if result['success']:
        fromDTP = 'info@discoverthepamirs.com' #'sales@discoverthepamirs.com'
        reciever_list= ('info@discoverthepamirs.com',) #info@discoverthepamirs.com
        # toDTP = 'info@discoverthepamirs.com'
        
        # Send a notofocation to client also

        
        message = "Your tour - "+ str(TourCode)+ \
        " ("+str(Title) + ") has a new request from "+str(firstname)+". \n\n" \
        "TOUR INFORMATION:\n" \
        "\nTour Code: "+ str(TourCode) \
        +"\nURL: https://discoverthepamirs.com"+str(TourURL) \
        +"\nDeparting Date: "+str(TourDeparture) \
        + "\n\nCUSTOMER DETAILS and INFORMATION:\n" \
        +"\nName: "+str(firstname)  \
        + "\nLast name: "+ str(lastname) \
        + "\nEmail: " + str(email)  \
        + "\nCountry: "+str(country) \
        + "\nPhone: " + str(phone) \
        + "\nChildren: "+ str(children) \
        + "\nAdults: "+str(adults) \
        + "\nMessage: "+str(message) \
        + " \n\nPlease reply to this message  during 24 hours. \n\n" \
        + "Best regards,\n\nThe Pakol Travel team"
        
        subject = 'Your tour - '+ str(TourCode) + ' - '+str(Title)+ ' has a new request from '+str(firstname) 

        send_mail(subject, message, fromDTP, reciever_list, fail_silently=False, )
        return HttpResponseRedirect('/tours/booking/success/')
    else:
        return HttpResponseRedirect('/error/')        
    #     else:
    #         return HttpResponseRedirect('/tours/invalid-booking-form/')
    # else:
    #     return HttpResponseRedirect('/tours/unknown-request-method/')


@login_required
def bookTourByDepartureID(request):
    if request.method == 'GET':
        form = BookTourByDepartureIDForm(request.GET)
        if form.is_valid():
            depid = form.cleaned_data['depid']
            depid = int(depid)
            departure = Departures.objects.get(id=depid)
            tid = departure.tour_id
            tour = Tour.objects.get(id=tid)
            tour.Route = tour.Route.split('-')
            thisTourDepartures = Departures.objects.filter(tour_id = tid)

            args = { 
                'tid':tid,
                'departure': departure,
                'tour': tour,
                'thisTourDepartures': thisTourDepartures, 
                }
            return render(request, 'tours/booking-form.html',  args)
    return HttpResponseRedirect('tours/enquire/error/')