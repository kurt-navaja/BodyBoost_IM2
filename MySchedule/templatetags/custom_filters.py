from django import template

register = template.Library()

@register.filter
def index(List, i):
    """
    Custom template filter to access list elements by index
    Usage in template: {{ my_list|index:forloop.counter0 }}
    """
    try:
        return List[int(i)]
    except (IndexError, ValueError, TypeError):
        return ''