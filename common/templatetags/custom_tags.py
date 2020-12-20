from django import template

register = template.Library()


@register.simple_tag(name='get_attr')
def get_attr(obj, attr, default=None):
    return getattr(obj, attr, default)