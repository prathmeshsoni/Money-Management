
from django import template

register = template.Library()

@register.simple_tag
def get_attribute(obj, attr_name):
    return getattr(obj, attr_name, "")