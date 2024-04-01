from django import template
register = template.Library()

@register.filter
def rating_iterator(number):
    return range(number)
	
