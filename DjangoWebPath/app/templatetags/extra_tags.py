from django import template
from app.models import *
register = template.Library()

@register.filter
def to_class_name(value):
    return value.__class__.__name__

@register.filter
def isinst(value, class_str):
    return isinstance(value, eval(class_str))