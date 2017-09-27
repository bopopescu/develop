from django import template

register = template.Library()

@register.filter(name = "cut_str")
def cut_str(value, flag):
    return value.split(flag)[-1]
     
