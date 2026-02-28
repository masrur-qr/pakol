from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from blog import views
from django.conf import settings
from django.conf.urls.static import static
from blog.views import tagged #, add_comment_to_post, comment_approve, comment_remove
# from django.shortcuts import redirect
# from django.views.generic import TemplateView 

app_name = 'blog'

urlpatterns = [
    # path('', views.blog_index, name='blog_index'), # the root index page
    # url(r'^$', views.blog_list, name="blog"),
    path('', views.blog_list, name="blog"),

    # url(r'^view-post-(?P<id>\d+)/(?P<Slug>[-\w+]+)/$', views.details, name='details'), #previous link
    url(r'^(?P<Slug>[-\w+]+)$', views.details, name='details'),
    
    # path('admin/', admin.site.urls),
    # path('', home_view, name="home"),
    path('post/<slug:slug>/', views.detail_view, name="detail"),
    path('tag/<slug:slug>/', views.tagged, name="tagged"),

    path('post/<int:id>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:id>/approve/', views.comment_approve, name='comment_approve'),
    path('comment/<int:id>/remove/', views.comment_remove, name='comment_remove'),

    # url(r'^tag/(?P<Slug>[-\w+]+)/$', tagged, name="tagged"),
    #Static pages
    # url(r'^about-us/$', TemplateView.as_view(template_name='discoverthepamirs/about-us.html'), name='about'),
] +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)#
