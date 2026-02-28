from django.contrib import admin
from tours.models import (Tour, 
                            Destination, Itinerary,  Departures, 
                            PlaceAvailability, Photo, Gallery,
                            TourActivities, TourTypes,
                         )
from django.contrib.auth.models import User
# Register your models here. 

class TourTypesAdmin(admin.ModelAdmin):
    list_display = ('Title', 'id', )
    list_filter =  ['Title',  ]
    # list_editable = ['Price', 'Available' ]
    prepopulated_fields = {'Slug':('Title',) }
# admin.site.register(TourTypes, TourTypesAdmin)

class TourActivitiesAdmin(admin.ModelAdmin):
    list_display = ('Title', 'id', )
    list_filter =  ['Title',  ]
    # list_editable = ['Price', 'Available' ]
    prepopulated_fields = {'Slug':('Title',) }
# admin.site.register(TourActivities, TourActivitiesAdmin)







class GalleryAdmin(admin.ModelAdmin):
    list_display = ('name','slug', 'tour')
    list_filter = ( 'name', 'created', )
    prepopulated_fields = {'slug':('name',)}

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('id', 'caption', 'gallery', 'image', )
    list_filter = ( 'gallery', 'created', 'updated' )
    search_fields = ('title','caption')
    prepopulated_fields = {'slug':('caption',)}

class ItineraryAdmin(admin.ModelAdmin):
    list_display = ('id','Title','tour',  )
    list_filter = ( 'tour', 'tour__TourCode', 'tour__Title', )
    # search_fields = ('ItineraryTitle',)
    # prepopulated_fields = {'slug':('title',)}

class PlaceAvailabilityInline(admin.TabularInline):
    # list_display = ('departures', 'BookedPlaces',  'AvailablePlaces', 'TotalPlaces',  )
    # list_filter = ('related_departure', 'departures',
    #      'departures__tour__TourCode','departures__tour__Title',)
    # list_editable = ['BookedPlaces',  'AvailablePlaces', 'TotalPlaces', ]
    model = PlaceAvailability
    extra = 0
# admin.site.register(PlaceAvailability, PlaceAvailabilityInline)
# admin.site.register(PlaceAvailability)

class DeparturesAdmin(admin.ModelAdmin):
    list_display = ('tour', 'DepartingDate','FinishingDate', 'tour_Duration', )
    list_filter = ('tour__Title', 
                    'tour__TourCode', 
                    'DepartingDate',
                    'FinishingDate', )
    list_editable = ['DepartingDate','FinishingDate', ]
    save_as = True
    def tour_Duration(self, obj):
        return str(obj.tour.Duration) + " days"
    
    # model = Departures
    # extra = 0
    inlines = [PlaceAvailabilityInline]
# admin.site.register(Departures, DeparturesAdmin)#(Category, CategoryAdmin)


class DestinationAdmin(admin.ModelAdmin):
    list_display = ('Title', 'Slug', )
    # list_editable = ['Price', 'Available' ]
    prepopulated_fields = {'Slug':('Title',) }
admin.site.register(Destination, DestinationAdmin)

class TourAdmin(admin.ModelAdmin):
    list_display = ('Title', 'TourCode',  'Available','Slug', )
    list_filter =  ['Title', 'TourCode', 'Available', 'Created', 'Updated', ]
    # list_editable = ['Price', 'Available' ]
    prepopulated_fields = {'Slug':('Title',) }
    # inlines = [DeparturesAdmin]
admin.site.register(Tour, TourAdmin)

admin.site.register(Itinerary, ItineraryAdmin)
admin.site.register(Photo, PhotoAdmin)
admin.site.register(Gallery, GalleryAdmin)#(Category, CategoryAdmin)




