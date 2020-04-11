from django import template
register = template.Library()


# Advert snippets
@register.inclusion_tag('search.html', takes_context=True)
def search(context):
    return {
        'select_properties': context['select_properties']
    }