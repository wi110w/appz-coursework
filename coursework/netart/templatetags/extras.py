from django import template
from urllib import parse

register = template.Library()


@register.filter()
def object_id(dict):
    return dict['_id']


@register.simple_tag(takes_context=True)
def url_replace(context, **kwargs):
    query = context['request'].GET.dict()
    query.update(kwargs)

    return parse.urlencode(query)