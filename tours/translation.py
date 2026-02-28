from modeltranslation.translator import translator, TranslationOptions
# from django.utils.translation import gettext_lazy  as _ # was gettext
from django.utils.translation import ugettext as _
from tours.models import (Tour,  
                        Destination, Itinerary,  Departures, 
                        PlaceAvailability, Photo, Gallery,
                        TourActivities, TourTypes
                         )

# from django.contrib.flatpages.models import FlatPage

class TourTranslationOptions(TranslationOptions):
    fields = ('Title', 'ShortDesc', 'Description',
        'Inclusions',
        'Exclusions',
        'Seasonality',
        'Highlights',
        'PriceList',
        'Route',
        'ImportantNotes',
        'StartingPoint',
        'EndingPoint',
    )
    fallback_values = {
        "Title": _("Не доступен на этом языке"),
    }
translator.register(Tour, TourTranslationOptions)

class DestinationTranslationOptions(TranslationOptions):
    fields = (
        'Country', 
        'Region', 
        'City',
        'Valley',
        'Village',
        'Area',
    )
    fallback_values = {
        "Area": _("Не доступен на этом языке"),
    }
translator.register(Destination, DestinationTranslationOptions)

class ItineraryTranslationOptions(TranslationOptions):
    fields = (
        'Title', 
        'Description',
    )
    fallback_values = {
        "Title": _("Не доступен на этом языке"),
    }
translator.register(Itinerary, ItineraryTranslationOptions)

class PhotoTranslationOptions(TranslationOptions):
    fields = (
        'caption', 
    )
    fallback_values = {
        "caption": _("Не доступен на этом языке"),
    }
translator.register(Photo, PhotoTranslationOptions)

class GalleryTranslationOptions(TranslationOptions):
    fields = (
        # 'name',
        'description',
    )
    fallback_values = {
        "description": _("Не доступен на этом языке"),
    }
translator.register(Gallery, GalleryTranslationOptions)


class TourActivitiesTranslationOptions(TranslationOptions):
    fields = (
        'Title',
    )
    fallback_values = {
        "Title": _("Не доступен на этом языке"),
    }
translator.register(TourActivities, TourActivitiesTranslationOptions)


class TourTypesTranslationOptions(TranslationOptions):
    fields = (
        'Title',
    )
    fallback_values = {
        "Title": _("Не доступен на этом языке"),
    }
translator.register(TourTypes, TourTypesTranslationOptions)