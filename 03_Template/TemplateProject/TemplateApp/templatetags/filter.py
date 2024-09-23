from django import template

register = template.Library()

@register.filter(name='status_to_string')
def convert_status_to_string(status, name):
    name = name.upper()
    if status == 10:
        return f'{name}: Success'
    elif status == 20:
        return f'{name}: Error'
    elif status == 30:
        return f'{name}: Pending'
    elif status == 40:
        return f'{name}: Failed'
    else:
        return f'{name}: Unknown'
