from django import template

register = template.Library()

def address(value, arg):
    add = value.split(',')
    if arg == 'landmark':
        return add[0]
    elif arg == 'city':
        return add[1]
    elif arg == 'state':
        return add[2]
    elif arg == 'country':
        return add[3]

register.filter('address' , address)
