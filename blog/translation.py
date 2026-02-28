from modeltranslation.translator import translator, TranslationOptions
from blog.models import Post
from django.utils.translation import gettext_lazy  as _ # was gettext
# from django.contrib.flatpages.models import FlatPage


class BlogPostTranslationOptions(TranslationOptions):
    fields = ('Title', 'ShortDesc', 'Content')
    # fallback_values = "-- Перевод недоступен -- " 
    fallback_values = {
        # "Title": _("Не доступен на этом языке"),
        "ShortDesc": None,
        "Content":_("Не доступен на этом языке"),
    }
translator.register(Post, BlogPostTranslationOptions)


# class FlatPageTranslationOptions(TranslationOptions):
#     fields = ('title', 'content', )
# translator.register(FlatPage, FlatPageTranslationOptions)