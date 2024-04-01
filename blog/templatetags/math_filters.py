from django import template
register = template.Library()

@register.filter
def sub(number_1,number_2):
    return number_1-number_2
	
