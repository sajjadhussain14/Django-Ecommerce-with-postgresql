from django import template

register = template.Library()

@register.filter
def get_nested_value(obj, keys):
    try:
        for key in keys.split('.'):
            obj = getattr(obj, key)
        return obj
    except (AttributeError, KeyError):
        return None