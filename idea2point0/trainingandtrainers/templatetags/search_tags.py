from django import template
from copy import deepcopy
register = template.Library()


# Advert snippets
@register.inclusion_tag('search.html', takes_context=True)
def search(context):
    select_properties = deepcopy(context['select_properties'])
    return {
        'select_properties': select_properties
    }