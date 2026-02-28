from django.db import models
from django.urls import reverse
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import User 
from django.conf import settings
from imagekit.processors import ResizeToFill  
from imagekit.models import ImageSpecField, ProcessedImageField   
from django.utils.translation import gettext_lazy  as _  
from django.utils import timezone
    
# Create your models here.
STATUS_CHOICES = (
    ('draft', 'Draft'),
    ('published', 'Published'),
)
POST_TYPE_CHOICES = (
    ('image', 'Image'),
    ('video', 'Video'),
)

PAGE_TEMPLATE_CHOICES = (
    ('about', 'home/about-us-template.html'),
    ('service', 'home/services-template.html'),
)


class Feedback(models.Model):
    Client = models.CharField(_("Client's name and surname"), max_length=60, blank=True, null=True,  default='', help_text="Enter the Title. Max: 60 characters")
    Content = models.TextField(_("Content"), max_length=165, blank=True, null=True, default='',help_text="Enter the content. Max: 165 characters")
    Image = ProcessedImageField(upload_to='feedbacks/%Y/',
                            processors=[ResizeToFill(300, 300)],
                            format='JPEG',
                            # options={'quality': 60}, 
                            blank=True)
    # Link = models.CharField("Link", max_length=100, blank=True, null=True, unique=True, help_text="Enter the link. Ex.: home-page or {% url 'home' %}")
    ProductTook = models.CharField("Product Took", max_length=55, blank=True, null=True,  default='Pamir Highway Tour', help_text="")
    Created = models.DateTimeField(auto_now_add=True)  
    Updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.Client)  
    
    class Meta:
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'

@receiver(post_delete, sender=Feedback)
def FeedbackImage_delete(sender, instance, **kwargs):
    instance.Image.delete(False)




class SEO_Optimiser(models.Model):
    Title = models.CharField(_("Title"), max_length=60, blank=True, null=True,  default='', help_text="Enter the Title. Max: 60 characters")
    Content = models.TextField(_("Content"), max_length=165, blank=True, null=True, default='',help_text="Enter the content. Max: 165 characters")
    Keywords = models.TextField('Keywords', max_length=200, blank=True, null=True, default='', help_text='Enter keywords, max 200 symbols' )
    Image = ProcessedImageField(upload_to='SEO/%Y/%m/%d/',
                            processors=[ResizeToFill(1200, 627)],
                            format='JPEG',
                            options={'quality': 60}, blank=True)
    # Link = models.CharField("Link", max_length=100, blank=True, null=True, unique=True, help_text="Enter the link. Ex.: home-page or {% url 'home' %}")
    PageName = models.CharField("Page Name", max_length=55, blank=True, null=True,  default='', help_text="This field is just for a note for the admins. For which page you want to add the SEO?")
    seoid = models.IntegerField("SEO id", default=0, blank=True, unique=True, null=True, help_text="This text is used in views.py")

    def __str__(self):
        return str(self.seoid) + " " +self.PageName
    
    class Meta:
        verbose_name = 'SEO Field'
        verbose_name_plural = 'SEO Fields'

@receiver(post_delete, sender=SEO_Optimiser)
def SEO_OptimiserImages_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.Image.delete(False)

class Page(models.Model):
    Title = models.CharField(_("Title"), blank=True, null=True, max_length=100, help_text="Enter the Title")
    # Slug = models.CharField(max_length=100, blank=True, null=True, unique=True, help_text="Enter the link. Ex.: eto-publikaciya")
    # ShortDesc = models.TextField("Short Desciption", max_length=165, null=True, blank=True, help_text="Enter the short description of the page using 165 symbols")
    Content = RichTextUploadingField("Content", blank=True, null=True, help_text="Введите контент")
    Image = ProcessedImageField(upload_to='pages/%Y/%m/%d/',
                            processors=[ResizeToFill(1200, 768)],
                            format='JPEG',
                            options={'quality': 60}, blank=True)
    image_thumbnail = ImageSpecField(source='Image',
                                 processors=[ResizeToFill(768, 500)],
                                 format='JPEG',
                                #  options={'quality': 60}
                                 )
    template = models.CharField('Template', max_length=20, blank=True, null=True, choices=PAGE_TEMPLATE_CHOICES, default='about', help_text='Select a template')                                 
    sortingIndex = models.IntegerField("Sorting Index",default=0, blank=True)
    SEO = models.ForeignKey(SEO_Optimiser, on_delete=models.CASCADE, null=True, blank=True)
    pageid = models.IntegerField("Page id", default=1, blank=True, help_text="This value is used in views.py")
    # seo_title = models.CharField(_("SEO Title"), max_length=60, blank=True, null=True,  default='', help_text="Enter the Title. Max: 60 characters")
    # seo_content = models.TextField(_("SEO Content"), max_length=165, blank=True, null=True, default='',help_text="Enter the content. Max: 165 characters")
    # seo_keywords = models.TextField('SEO Keywords', max_length=200, blank=True, null=True, default='', help_text='Enter keywords, max 200 symbols' )
    Created = models.DateTimeField(auto_now_add=True)  
    Updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='published')

    def __str__(self):
        return self.Title
    
    class Meta:
        ordering = (('-Created'),)
        # index_together = (('id', 'Slug'),)
        verbose_name = 'Page'
        verbose_name_plural = 'Pages'

        
class FAQ(models.Model):
    Title = models.CharField(max_length=300, blank=True, null=True,  help_text="Enter the Title. Max: 200 characters")
    Content = RichTextUploadingField("Content", blank=True, null=True, default='',help_text="Enter the content.")
    sortingIndex = models.IntegerField("Sorting Index",default=0, blank=True)

    def __str__(self):
        return self.Title
    
    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'


class RentalsAndServices(Page):
    # pass
    Slug = models.CharField(max_length=100, blank=True, null=True, unique=True, help_text="Enter the link. Ex.: eto-publikaciya")
    ShortDesc = models.TextField("Short Desciption", max_length=165, null=True, blank=True, help_text="Enter the short description of the page using 165 symbols")
    
    def __str__(self):
        # super().__init__()  # self.Title
        return self.Title
    

    class Meta:#(Page.Meta)
        verbose_name = 'Rentals and Services'
        verbose_name_plural = 'Rentals and Services'
    
    def get_absolute_url(self):
        return reverse('home:serviceRentalDetails', args = [self.Slug]) 


