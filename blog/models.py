from django.db import models
from django.urls import reverse
from django.urls import reverse
from django.template.defaultfilters import slugify
from ckeditor.fields import RichTextField
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import User 
from django.utils import timezone

#Gallery imports
from django.db.models.signals import post_delete
from django.dispatch.dispatcher import receiver
from imagekit.models import ImageSpecField # < import this
from imagekit.processors import ResizeToFill # < import this
from imagekit.models import ImageSpecField, ProcessedImageField # resize

from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from django import forms

# Create your models here.

class TaggedPost(TaggedItemBase):
    content_object = models.ForeignKey('Post', on_delete=models.CASCADE)

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    POST_TYPE_CHOICES = (
        ('image', 'Image'),
        ('video', 'Video'),
    ) 
    # category = models.ForeignKey(Category, on_delete=models.PROTECT) 
    Title = models.CharField("Post Title", max_length=300, help_text="Enter the title of the post.")
    Slug = models.SlugField(max_length=300, blank=True, unique=True, help_text="Slug is what is seen in the URL. Ex. this-is-a-post")
    # Category = models.CharField("News Category", max_length=200, choices = NEWSCATEGORY, help_text="Select from the list")
    ShortDesc = models.TextField("Short Description", blank=True, help_text="Enter the short description of the post here")
    Content = RichTextField("Post content", help_text="Enter the post content")
    # author = models.ForeignKey(User, on_delete=models.PROTECT) #related_name='news_posts',
    author =  models.CharField("Author", max_length=30, default="Admin", help_text="Enter the author.")
    # Image = models.ImageField(upload_to='news_image/', blank=True)
    posttype = models.CharField(max_length=10, choices=POST_TYPE_CHOICES, default='image')     
    Image = ProcessedImageField(upload_to='blog/%Y/%m/%d/',
                            processors=[ResizeToFill(1200, 768)],
                            format='JPEG',
                            options={'quality': 60}, blank=False)
    image_thumbnail = ImageSpecField(source='Image',
                                 processors=[ResizeToFill(768, 500)],
                                 format='JPEG',
                                #  options={'quality': 60}
                                 )
    VideoEmbedCode = models.TextField("Video Embed Code", blank=True, help_text="Enter the Video Embed Code here") 
    #VideoEmbedCode = RichTextField("Video Embed Code", help_text="Enter the VideoEmbedCode")  

    published = models.DateTimeField(auto_now=True)
    tags = TaggableManager(through=TaggedPost, blank=True)
    allow_commenting = models.BooleanField(default=True)
    hide_comments = models.BooleanField(default=False)
    # blog_views=models.IntegerField(default=0)
    Created = models.DateTimeField(default=timezone.now ) #auto_now_add=True, 
    # Created.editable=True
    Updated = models.DateTimeField(auto_now=True)
    # Updated.editable=True
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')

    def __str__(self):
        return "Post #"+str(self.id) +" - "+ self.Title
    
    def get_absolute_url(self):
#        return reverse('blog:details', args = [self.id, self.Slug]) 
        return reverse('blog:details', args = [self.Slug]) 

    def save(self, *args, **kwargs):
        if not self.id:
            # Newly created object, so set slug
            self.Slug = slugify(self.Title)
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = (('-Created'),)
        index_together = (('id', 'Slug'),)

class Comment(models.Model):
    post = models.ForeignKey('blog.Post', on_delete=models.CASCADE, related_name='comments')
    author = models.CharField(max_length=200, blank=True)
    owner = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)# related_name='user_comments', on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_user', default='Saidmamad')
    # models.ForeignKey(TourOperator, on_delete=models.PROTECT)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()
    
    class Meta:
        ordering = (('-created_date'),)

    def __str__(self):
        return 'Approved:'+str(self.approved_comment) + '; '+ self.text


class CommentForm(forms.ModelForm):
    # author = forms.CharField(max_length=255)
    # owner = forms.CharField(max_length=200) #,  widget=forms.HiddenInput()
    text = forms.CharField(widget=forms.Textarea)
    # created_date = forms.DateField()
    # approved_comment = forms.BooleanField()
    
    class Meta:
        model = Comment
        fields = (
            # 'author',
            # 'user',
            # 'owner', 
            'text',
        )





@receiver(post_delete, sender=Post)
def post_image_delete(sender, instance, **kwargs):
    # Pass false so FileField doesn't save the model.
    instance.Image.delete(False)

# @receiver(pre_save, sender=Photo)
# def make_thumbnail(sender, instance, **kwargs):
#     easy_thumbnails.files.generate_all_aliases(instance.image, False)