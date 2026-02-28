from django.db import models
from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.urls import reverse
from django.views.generic import TemplateView
from django.template.defaultfilters import slugify

from django.core.exceptions import ValidationError

#Gallery imports
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from imagekit.models import ImageSpecField # < import this
from imagekit.processors import ResizeToFill # < import this
from imagekit.models import ImageSpecField,  ProcessedImageField # resize
# from imagekit.processors import * #new

import datetime
from django.utils.translation import ugettext as _


from multiselectfield import MultiSelectField
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from datetime import datetime 
from django.utils.timezone import now
from home.models import SEO_Optimiser
# Create your models here. 

DESTINATIONS = (
    ('pamir', _('Pamir')),
    ('nothern-tajikistan', _('Nothern-Tajikistan')),
    ('southern-tajikistan', _('Southern-Tajikistan')),
    ('dushanbe-and-surroundings', _('Dushanbe & surroundings')),
    ('afghanistan-wakhan', _('Afghanistan Wakhan')),
    ('rasht-valley', _('Rasht Valley')),
    

)
STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),  
    )
    
# TOUR_TYPES = (
#     ('Group Tour', _('Group Tour')),
#     ('Private Tour', _('Private Tour')),
#     ('Day Tour', _('Day Tour')),
#     ('MultidayT our', _('Multiday Tour')),
# )



TITLE_CHOICES = (
    ('MR', 'Mr.'),
    ('MRS', 'Mrs.'),
    ('MS', 'Ms.'),
    )

NUMCHOICE10 = (
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 4),
    (5, 5),
    (6, 6),
    (7, 7),
    (8, 8),
    (9, 9),
    (10, 10),
    )

class Gallery(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    # image = models.ImageField(upload_to="photogalleries/galleries/")
    image = ProcessedImageField(blank=True, upload_to='photogalleries/galleries/',
                            processors=[ResizeToFill(400, 250)],
                            format='JPEG',
                            options={'quality': 60})
    image_thumbnail = ImageSpecField(source='image',
                                 processors=[ResizeToFill(200, 150)],
                                 format='JPEG',
                                #  options={'quality': 60}
                                 )  
    description = models.CharField("Description", blank=True, max_length=300, help_text="Enter the description of the album.")
    published = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')


    class Meta:
        ordering = ('name',)
        verbose_name = 'Gallery'
        verbose_name_plural = 'Galleries' 

    def get_absolute_url(self):
        return reverse('viewPhoto', args = [self.id, self.slug])

    def __str__(self):
        return self.name





# #using callable cache_to use the new file name changed by callable upload_to method and put it in "thums" folder
def cache_to_thumb(instance, path, specname, extension):
     path="photogalleries/"+instance.gallery.name+"/thumbs/"+instance.filename()
     return path

def get_path(instance, filename):
    extension = filename.rsplit('.', 1)[1]      
    directory = "photogalleries/galleries/"+instance.gallery.slug+"/bigs/"      
    name = instance.slug
    return "%s/%s.%s" % (directory, name, extension)

class Photo(models.Model):
    gallery =  models.ForeignKey(Gallery, on_delete=models.CASCADE)
    # image = models.ImageField(upload_to='photogalleries/photos/%Y/%m/%d/')
    # photogalleries/photos/%Y/%m/%d/
    image = ProcessedImageField(upload_to=get_path,
                            processors=[ResizeToFill(1200, 768)],
                            format='JPEG',
                            options={'quality': 60})
    image_thumbnail = ImageSpecField(source='image',
                                processors=[ResizeToFill(248, 165)],
                                format='JPEG',
                                options={'quality': 60},
                                # upload_to=cache_to_thumb # old version 
                                ) 
    # title = models.CharField(max_length=150)
    caption = models.CharField(max_length=300, blank=False)
    slug = models.SlugField(max_length=100, unique=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    orderingIndex = models.IntegerField(default=0, help_text="Used for ordering teh image in the album from smaller to bigger digit")  


    def __str__(self):
        return str(self.id) +" - "+ self.caption

    # def user_directory_path(instance, filename):
    #     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    #     return 'user_{0}/{1}'.format(instance.user.id, filename)


    def get_absolute_url(self):
        return reverse('viewPhoto', args = [self.id, self.slug])

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.Slug = slugify(self.caption)
        super(Photo, self).save(*args, **kwargs)

    class Meta:
        ordering = (('orderingIndex'),  ('created'),)
        index_together = (('id', 'slug'),)

# @receiver(post_init, sender=Photo)
# def post_init_receiver(sender, instance, **kwargs):
#     pass    

# @receiver(post_save, sender=Photo)
# def post_save_receiver(sender, instance=None, created=False, raw=False, **kwargs):
#     if not raw:       
#         instance.image_thumbnail.invalidate()

# @receiver(post_save, sender=Photo)
# #I am calling myspec without invalidating anything
# def post_save_receiver(sender, instance=None, created=False, raw=False, **kwargs):
#       instance.image_thumbnail.url


class TaggedTour(TaggedItemBase):
    content_object = models.ForeignKey('Tour', on_delete=models.CASCADE)


class TourActivities(models.Model):
    Title = models.CharField('Activity', max_length=50, default='', blank=True)
    Slug = models.SlugField('Slug',max_length=100, blank=True, unique=False, default='', help_text='Do not change it!') #False?
    sortingIndex = models.IntegerField(default=0)
    
    def __str__(self):
        return self.Title
    
    # class Meta:
    #     #db_table = 'tour_activities'
        # verbose_name = _("Essay style question")
        # ordering = (('orderingIndex'), ('-tour'), ('Title'))
        # verbose_name_plural = ("Itineraries")

class TourTypes(models.Model):
    Title = models.CharField(max_length=100, default='', blank=True)
    Slug = models.SlugField(max_length=100, blank=True, default='',  help_text='Do not change it!') #False?
    sortingIndex = models.IntegerField(default=0)
    
    def __str__(self):
        return self.Title

ACTIVITIES = (
    ('jeep-tours', _('Jeep Tours')),
    ('cultural-tours', _('Cultural Tours')),
    ('trekking-and-hiking', _('Trekking & Hiking')),
    ('cycling-tours', _('Cycling Tours')),
    ('city-tours', _('City Tours')),
    ('wildlife-tours', _('Wildlife Tours')),
)


# Darkor nist 
class Destination(models.Model):
    Title = models.CharField("Destination title", max_length=100, blank = True, help_text="Pamir")
    Slug = models.SlugField('Slug',max_length=100, blank=True, unique=True, default='', help_text='Do not change it!') #False?
    ShortDesc = models.TextField("Short Desciption", max_length=165, null=True, blank=True, help_text="Used on photos ")
    Content = RichTextUploadingField("Content", blank=True, null=True, help_text="Введите контент")
    Image = ProcessedImageField(upload_to='destinations/',
                            processors=[ResizeToFill(1200, 768)],
                            format='JPEG',
                            options={'quality': 60}, blank=True)
    image_thumbnail = ImageSpecField(source='Image',
                                 processors=[ResizeToFill(768, 500)],
                                 format='JPEG',
                                #  options={'quality': 60}
                                 )
    sortingIndex = models.IntegerField("Sorting Index",default=0, blank=True)
    # SEO = models.ForeignKey(SEO_Optimiser, on_delete=models.CASCADE, null=True, blank=True)
    # pageid = models.IntegerField("Page id", default=1, blank=True, help_text="This value is used in views.py")
    start_price = models.IntegerField("Starting Price", default=99, blank=True, help_text="Starting price in the destination")
    # seo_title = models.CharField(_("SEO Title"), max_length=60, blank=True, null=True,  default='', help_text="Enter the Title. Max: 60 characters")
    # seo_content = models.TextField(_("SEO Content"), max_length=165, blank=True, null=True, default='',help_text="Enter the content. Max: 165 characters")
    # seo_keywords = models.TextField('SEO Keywords', max_length=200, blank=True, null=True, default='', help_text='Enter keywords, max 200 symbols' )
    SEO = models.ForeignKey(SEO_Optimiser, on_delete=models.CASCADE, null=True, blank=True)

    Created = models.DateTimeField(auto_now_add=True, blank=True)  #auto_now_add=True,
    Updated = models.DateTimeField(auto_now=True, blank=True) #auto_now=True,
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')
    
 
    def __str__(self):
        return str(self.Title) #str(self.id) + '-'+ self.Area + ', '+ self.Country

    def get_absolute_url(self):
        return reverse('home:destinationViewer', args = [self.Slug]) 

@receiver(post_delete, sender=Destination)
def DestinationImages_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.Image.delete(False)


class Tour(models.Model):
    
    # TourOperator = models.ForeignKey(TourOperator, on_delete=models.PROTECT)
    Destination = models.ForeignKey(Destination, on_delete=models.PROTECT, blank=True, null=True, )
    TourCode = models.CharField(max_length=10, unique=True, help_text='Ex. JT001 ') #user = models.OneToOneField(User)
    Title = models.CharField(max_length=200, help_text="Title of the tour here")
    Slug = models.SlugField(max_length=300, blank=True, unique=True, editable=True) #False?
    # TourType = MultiSelectField("Tour Type", choices = ACTIVITIES, null=True, blank=True, help_text="Check any that applies to your tour")
    TourType = models.CharField("Tour Type", max_length=20, choices = ACTIVITIES, null=True, blank=True, help_text="Check any that applies to your tour")

    # tourActivities = models.ManyToManyField(TourActivities, blank=True,   related_name="tourActivities")
    # Destination = MultiSelectField("Destination", choices = DESTINATIONS, null=True, blank=True, help_text="Select destinations")
    # Activities = MultiSelectField(choices = ACTIVITIES, help_text="Check any that applies to your tour")
    # tourTypes = models.ManyToManyField(TourTypes, blank=True,  related_name="tourTypes")
    Duration = models.IntegerField(default=0)
    ShortDesc = models.TextField("Short Description", max_length=165, blank=True, default='', help_text='Short description')
    # Description = models.TextField(help_text='Description of the tour...')
    Description = RichTextUploadingField("Description", blank=True, null=True, help_text="Long description of the tour...")

    Inclusions = models.TextField(help_text="Inclusions of the tour")
    Exclusions = models.TextField(help_text="Exclusions of the tour; Seperate them with semicolon")
    # Difficulty = models.IntegerField(help_text="Enter a value between 1 to 10", choices=NUMCHOICE10, default=5)
    GroupSize = models.CharField("Group size",max_length=2, blank=True, help_text="Group size")
    Seasonality = models.CharField(max_length=100, help_text="Seasonality of the tour; Ex. July - September")
    Highlights = models.TextField(help_text="Highlights of the tour. Seperate with semicolon. Ex. Yamchun fortress; etc")
    Price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    PriceList = models.TextField(help_text="Price List", blank=True)
    Image = ProcessedImageField(upload_to='tours/main-image/%Y/%m/%d/',
                            processors=[ResizeToFill(1200, 768)],
                            format='JPEG',
                            options={'quality': 60})
    image_thumbnail = ImageSpecField(source='Image',
                                 processors=[ResizeToFill(768, 500)],
                                 format='JPEG',
                                #  options={'quality': 60}
                                 ) 
    Created = models.DateTimeField(auto_now_add=True)
    Updated = models.DateTimeField(auto_now=True)
    Available = models.BooleanField(default=True)
    # Rating = models.IntegerField(default=5, choices=NUMCHOICE10)
    Route = models.CharField(max_length=400, help_text='Route. Example: Dushanbe - Murghab- Osh', blank=True)
    Gallery =  models.OneToOneField(Gallery, null=True, on_delete=models.PROTECT, blank=True)
    ImportantNotes = models.TextField("Important Notes", help_text="Seperate the important notes with semicolons.", blank=True)
    NumberOfDays = models.IntegerField("Number Of Days",default=5, help_text='Enter the number of days')
    NumberOfNights = models.IntegerField("Number Of Nights", default=5, help_text='Enter the number of nights')
    StartingPoint = models.CharField("Starting Point",max_length=50, default="Dushanbe", help_text="Starting point. Ex. Dushanbe, Tajikistan")
    EndingPoint = models.CharField("Ending Point", max_length=50,  default="Dushanbe", help_text="Ending point. Ex. Dushanbe, Tajikistan")
    Approved_tour =  models.BooleanField(default=False)
    # Offer = models.BooleanField(default=False, help_text="Tick it when you want the tour to show in offered tour list")
    # Discount = models.FloatField(blank=True, default=0, help_text='Enter discount. Ex. 10')
    # Deposit = models.FloatField(blank=True, default=0.0, help_text='Enter deposit. Ex. 100')
    # adminNotes = models.TextField("Admin Notes", help_text="This field is just for admin. Users don't see it", blank=True, default='')

    # tags = TaggableManager(through=TaggedTour)
    Status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    sortingIndex = models.IntegerField(default=0)

    class Meta:
        ordering = (('sortingIndex'), ('-Created'),)
        index_together = (('id', 'Slug'),)

    def __str__(self):
        return self.TourCode + '-'+ self.Title #+ '  -- (owner: '+ str(self.TourOperator)+' )'
    
    def clean_Title(self):
        return self.cleaned_data['Title'] or None

    def get_absolute_url(self):
        return reverse('tours:details', args = [self.Slug]) 

    # def get_TourOperator(self):
    #     return self.TourOperator

    def get_Destination(self):
        return self.Destination

    def save(self, *args, **kwargs):
            """
            This function slugifies the Title
            """
            if not self.id:
                # Newly created object, so set slug
                self.Slug = slugify(self.Title)
            super(Tour, self).save(*args, **kwargs)

    # def get_Destination(self):
    #     destination = Destination.objects.all()
    #     return self.Destination.Country

class Itinerary(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="tour_itineraries" )
    Title = models.CharField("Itinerary Title",max_length=200, help_text="Example: Day 01: Arrival in Dushanbe ")
    Image = ProcessedImageField(upload_to='tours/itineraries/%Y/%m/%d/',
                            processors=[ResizeToFill(400, 250)],
                            format='JPEG',
                            options={'quality': 60},
                            blank=True,
                            )
    Description = models.TextField("Itinerary Description", help_text='Description of the day')
    orderingIndex = models.IntegerField(default=0, help_text="Used for ordering teh image in the album from smaller to bigger digit")  


    class Meta:
        # db_table = Itineraries
        # verbose_name = _("Essay style question")
        ordering = (('id'),) #(('orderingIndex'), ('-tour'), ('Title'))
        verbose_name_plural = ("Itineraries")

    def __str__(self):
        return str(self.tour) + " | " + self.Title
        


class Departures(models.Model):
    tour = models.ForeignKey(Tour, on_delete=models.CASCADE, related_name="tour_departures")
    DepartingDate = models.DateField(auto_now=False,blank= True,null=True)
    FinishingDate = models.DateField(auto_now=False,blank= True,null=True)
    # DepartureStatus = models.CharField(max_length=200, choices = DEPARTURE_STATUS, help_text="Select from the list")
    # PlaceAvailability = models.ForeignKey(PlaceAvailability, on_delete=models.CASCADE)
    # DepartureGaranteed = models.BooleanField("Departure Garanteed", default="True")
    

    def __str__(self):
        return str(self.tour) +" | "+ str(self.DepartingDate)+ ' to ' + str(self.FinishingDate)
    
    class Meta:
        ordering = (('-tour'), ('DepartingDate'))
        verbose_name_plural = "Departures"

class PlaceAvailability(models.Model):
    departures = models.OneToOneField(Departures, on_delete=models.CASCADE, primary_key=True, related_name="departure_place_availability")
    BookedPlaces = models.IntegerField("Booked places", blank=True)
    AvailablePlaces = models.IntegerField("Available Places", blank=True)
    TotalPlaces = models.IntegerField("Total Places", blank=True)

    class Meta:
        verbose_name_plural = "Place Availability"

    def __str__(self):
        return str(self.departures) +" ==> Booked:"+ str(self.BookedPlaces)+ " Available:"+ str(self.AvailablePlaces)
    

    def place_is_available(self):
        result = (self.BookedPlaces < self.TotalPlaces)  
        return result

    def clean(self):
        # if not self.places_is_available():
        #     raise ValidationError('No more places available for booking! Check other departures please!')
        #     '''
        #     Include from django.core.exceptions import ValidationError
        #     Note:
        #     Above 'forms.ValidationError' I think will work for HTML forms purposes 
        #     '''
        if self.BookedPlaces > self.TotalPlaces:
            raise ValidationError("No more places available for booking! Check other departures please!")
        
        if self.BookedPlaces < 0:
            raise ValidationError("Booked Places cannot be negative!")
        
        if self.AvailablePlaces < 0:
            raise ValidationError("Available Places cannot be negative!")

        if self.BookedPlaces + self.AvailablePlaces > self.TotalPlaces:
            raise ValidationError("Error! Sum of 'Booked Places' and 'Available Places' cannor be more than 'Total Places'")

    # def save(self, *args, **kwargs):
    #     if(self.BookedPlaces < self.TotalPlaces):
    #         super(PlaceAvailability, self).save(*args, **kwargs)
    #     else:
    #         raise forms.ValidationError('Sorry! There arent places anymore. ')


@receiver(post_delete, sender=Gallery)
def album_image_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.image.delete(False)
    # instance.ImageCacheFiles.delete(False)
    # instance.image_thumbnail.delete(False)

@receiver(post_delete, sender=Photo)
def image_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.image.delete(False)
    # instance.ImageCacheFiles.delete(False)
    # instance.image_thumbnail.delete(False)

@receiver(post_delete, sender=Itinerary)
def Image_delete(sender, instance, **kwargs):
    instance.Image.delete(False)

@receiver(post_delete, sender=Tour)
def TourImages_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.Image.delete(False)
    

class SearchForm(forms.Form):
    # Country = forms.CharField(max_length=255, initial='')
    # TourType = forms.CharField(max_length=255, initial='')
    # Destination = forms.CharField(max_length=255, initial='') #, blank=True
    # StartDate = forms.DateField()
    TourType = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        # choices=TOUR_TYPES, 
        # choices=TourTypes.objects.all() 

        # initial='',
    )
    Activities = forms.MultipleChoiceField(
        required=False,
        widget=forms.CheckboxSelectMultiple,
        # choices=ACTIVITIES,
        # initial='',
    )
    Title = forms.CharField(max_length=255, required=False)
    DepartingDate = forms.CharField(required=False)
    FinishingDate = forms.CharField(required=False)
    MinPrice = forms.IntegerField(required=False)
    MaxPrice = forms.IntegerField(required=False)

    # Destination = forms.CharField(max_length=255, initial='')
    # Area = forms.CharField(max_length=255, initial='')


class BookTourForm(forms.Form):
    TourDeparture = forms.CharField(max_length=255, required=True)
    firstname = forms.CharField(max_length=255, required=True)
    lastname = forms.CharField(max_length=255, required=True )
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=255, required=False)
    country = forms.CharField(max_length=255, required=False)
    adults = forms.IntegerField(required=False)
    children = forms.IntegerField(required=False)
    message = forms.CharField(max_length=255, required=False)
    TourCode = forms.CharField(max_length=255, required=False)
    Title = forms.CharField(max_length=255, required=False)
    TourURL = forms.CharField(max_length=255, required=False)
    TourDeparture = forms.CharField(max_length=255, required=False) # Problem ??

class BookThisForm(forms.Form):
    tid = forms.CharField(max_length=10) 

class BookTourByDepartureIDForm(forms.Form):
    depid = forms.IntegerField()