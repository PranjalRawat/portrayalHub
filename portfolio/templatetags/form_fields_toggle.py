# custom_filters.py
from django import template

register = template.Library()

@register.filter
def add_disabled(form):
    """
    Add 'disabled' attribute to the field if it's disabled.
    """
    for field in form:
        if field.field:
            field.field.widget.attrs['disabled'] = True
    return form.as_p()

@register.filter
def remove_disabled(form):
    """
    Remove 'disabled' attribute to the field if it's disabled.
    """
    for field in form:
        if field.field:
            field.field.widget.attrs['disabled'] = False
    return form.as_p()