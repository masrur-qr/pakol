from django.contrib import admin
from home.models import *
                        # (
                        # Page, 
                        # # ServiceList, 
                        # SEO_Optimiser,
                        # # HowDoesItWork, 
                        # FAQ,
                        # )
# Register your models here.

class PageAdmin(admin.ModelAdmin):
    list_display = ('Title', 'pageid',   'template' )
    list_filter =  [
        'Title', 
        'Created', 
        'Updated',
    ]
    list_editable = ['pageid', ]
    # prepopulated_fields = {'Slug':('Title',) }
admin.site.register(Page, PageAdmin)

class SEOAdmin(admin.ModelAdmin):
    list_display = ( 'PageName','Title', 'id', 'seoid', 'Image' )
    list_filter =  ['PageName', 'Title', ]
    save_as = True
    list_editable = ['seoid', ]

    # readonly_fields = ("PageName", 'id')
admin.site.register(SEO_Optimiser, SEOAdmin)

class FAQAdmin(admin.ModelAdmin):
    list_display = ('Title', 'id', )
    list_filter =  ['Title', ]
admin.site.register(FAQ, FAQAdmin)


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('Client', )
    # list_filter =  ['Title', ]
admin.site.register(Feedback, FeedbackAdmin)


class RentalsAndServicesAdmin(admin.ModelAdmin):
    list_display = ('Title', 'Slug')
    prepopulated_fields = {'Slug':('Title',) }
    # list_filter =  ['Title', ]
    save_as = True

admin.site.register(RentalsAndServices, RentalsAndServicesAdmin)