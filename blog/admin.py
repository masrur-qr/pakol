from django.contrib import admin
from blog.models import Post, Comment
# from modeltranslation.admin import TranslationAdmin 

# # Register your models here.

# class PostAdmin(admin.ModelAdmin):
#     list_display = ('Title', 'author', 'published', 'status')
#     list_filter = ('status', 'Created', 'published', 'author')
#     search_fields = ('Title', 'Content')
#     prepopulated_fields = {'Slug':('Title',)}

# admin.site.register(Post, PostAdmin)
# admin.site.register(Comment)

class PostAdmin(admin.ModelAdmin): #TranslationAdmin
    list_display = ('Title', 'Slug', 'status')
    list_filter = ('status', 'Created',    )
    search_fields = ('Title', )
    prepopulated_fields = {'Slug':('Title',)}
admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
