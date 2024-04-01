from django import template
register = template.Library()

@register.filter
def query_len(query):
    return len(query)
	