from django.template import Library

register = Library()

@register.filter(name='f_class')
def f_class(value, arg):
    return value.as_widget(attrs={'class': arg})