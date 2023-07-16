from django import template

register = template.Library()

@register.filter
def get_attribute(obj, attr_name):
    return getattr(obj, attr_name, None)
