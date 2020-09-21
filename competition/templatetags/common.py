from django import template

register = template.Library()


@register.simple_tag
def text_size(text: str):
    result = 34
    if len(text) < result:
        result = result - len(text)
    return f'{result}px'


@register.simple_tag
def get_index(_list, index):
    try:
        return _list[index]
    except IndexError:
        return '-'


@register.filter(name='m_index')
def index(_list, ind):
    result = '-'
    if ind >= 0:
        try:
            result = _list[ind]
        except IndexError:
            pass
    return result
