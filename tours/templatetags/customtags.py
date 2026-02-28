from django import template

register = template.Library()
from django.template import Library;register = Library()

@register.filter
def get_list(dictionary, key):
    return dictionary.getlist(key)

@register.filter(name='split')
def split(value, key):
    """
        Returns the value turned into a list.
    """
    return value.split(key)

@register.filter(name='range') 
def filter_range(start, end):
    return range(start,end)